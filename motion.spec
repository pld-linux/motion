#
# Conditional builds:
%bcond_without	pgsql		# build PostgreSQL support
%bcond_without	mysql		# build MySQL support
%bcond_without	sqlite		# build SQLite support
%bcond_without	xmlrpc		# build XMLRPC support 
%bcond_without	v4l		# build v4l support 
#
Summary:	Motion is a software motion detector
Summary(pl.UTF-8):	Motion - programowy wykrywacz ruchu
Name:		motion
Version:	4.0.1
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	https://github.com/Motion-Project/motion/archive/release-%{version}.tar.gz
# Source0-md5:	5c87f90c4118d8cf0fb14700db69118f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
URL:		https://motion-project.github.io/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel >= 0.7.1
BuildRequires:	libjpeg-devel
%{?with_mysql:BuildRequires:    mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Motion is a software motion detector. It grabs images from video4linux
devices and/or from webcams (such as the axis network cameras). Motion
is the perfect tool for keeping an eye on your property keeping only
those images that are interesting.

%description -l pl.UTF-8
Motion to programowy wykrywacz ruchu. Przechwytuje obrazy z urządzeń
video4linux i/lib kamer (takich jak kamery sieciowe axis). Motion jest
doskonałym narzędziem do doglądania swojej posiadłości, przechowując
tylko interesujące obrazy.

%package init
Summary:	Init script for Motion
Summary(pl.UTF-8):	Skrypt init dla systemu Motion
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Provides:	group(motion)
Provides:	user(motion)

%description init
Init script for Motion.

%description init -l pl.UTF-8
Skrypt init dla systemu Motion.

%prep
%setup -q  -n motion-release-%{version}

%build
autoreconf -fvi
%configure \
	--without-optimizecpu \
	%{?!with_mysql:--without-mysql} \
	%{?!with_pgsql:--without-pgsql} \
	%{?!with_sqlite:--without-pgsql} \
	%{?!with_v4l:--without-v4l}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT/var/run/%{name} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/doc doc
mv $RPM_BUILD_ROOT%{_sysconfdir}/motion/motion-dist.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/motion/motion.conf

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/motion/camera*

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT


%pre init
%groupadd -g 177 motion
%useradd -u 177 -g motion motion
/usr/sbin/usermod -G video motion 1>&2 > /dev/null

%post init
/sbin/chkconfig --add motion
%service motion restart

%preun init
if [ "$1" = "0" ]; then
	%service motion stop
	/sbin/chkconfig --del motion
fi

%postun init
if [ "$1" = "0" ]; then
	%userremove motion
	%groupremove motion
fi

%triggerpostun -- motion < 3.2.6-1
if [ -e /etc/motion.conf.rpmsave ]; then
	cp /etc/motion/motion.conf /etc/motion/motion.conf.rpmnew
	cp /etc/motion.conf.rpmsave /etc/motion/motion.conf
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS FAQ README.md motion_guide.html *.conf
%attr(755,root,root) %{_bindir}/motion
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/motion/motion.conf
/usr/lib/tmpfiles.d/%{name}.conf
%{_datadir}/motion
%{_mandir}/man1/*
%attr(750,motion,motion) %dir /var/run/%{name}

%files init
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
