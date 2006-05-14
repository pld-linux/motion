# TODO:
# - init subpackage should have own user. Current solution isn't safe.
# - change default configuration for existing directories
#
# Conditional builds:
%bcond_without	pgsql		# build PostgreSQL support
%bcond_without	mysql		# build MySQL support
%bcond_without	xmlrpc		# build XMLRPC support 
#
Summary:	Motion is a software motion detector
Summary(pl):	Motion - programowy wykrywacz ruchu
Name:		motion
Version:	3.2.6
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	http://dl.sourceforge.net/motion/%{name}-%{version}.tar.gz
# Source0-md5:	71e6bd13fcca70372e9b7c7806d62b30
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.lavrsen.dk/twiki/bin/view/Motion/WebHome
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel >= 0.4.8
BuildRequires:	libjpeg-devel
%{?with_mysql:BuildRequires:    mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Motion is a software motion detector. It grabs images from video4linux
devices and/or from webcams (such as the axis network cameras). Motion
is the perfect tool for keeping an eye on your property keeping only
those images that are interesting.

%description -l pl
Motion to programowy wykrywacz ruchu. Przechwytuje obrazy z urz±dzeñ
video4linux i/lib kamer (takich jak kamery sieciowe axis). Motion jest
doskona³ym narzêdziem do dogl±dania swojej posiad³o¶ci, przechowuj±c
tylko interesuj±ce obrazy.

%package init
Summary:	Init script for Motion
Summary(pl):	Skrypt init dla systemu Motion
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description init
Init script for Motion.

%description init -l pl
Skrypt init dla systemu Motion.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-libavcodec=%{_libdir} \
	--without-optimizecpu \
	%{?with_mysql:--with-mysql} \
	%{?with_pgsql:--with-pgsql}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
$RPM_BUILD_ROOT{%{_datadir}/%{name},%{_examplesdir}/%{name}-%{version},%{_sysconfdir}/%{name}} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/doc doc
mv $RPM_BUILD_ROOT%{_sysconfdir}/motion-dist.conf $RPM_BUILD_ROOT%{_sysconfdir}/motion.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add motion
%service motion restart

%preun init
if [ "$1" = "0" ]; then
	%service motion stop
	/sbin/chkconfig --del motion
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS FAQ README README.axis_2100 motion_guide.html *.conf motion.init-RH
%attr(755,root,root) %{_bindir}/motion
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/motion.conf
%dir %{_sysconfdir}/%{name}
%{_datadir}/motion
%{_mandir}/man1/*

%files init
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
