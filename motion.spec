#
# Conditional builds:
%bcond_without	pgsql		# build PostgreSQL support
%bcond_without	mysql		# build MySQL support
%bcond_without	xmlrpc		# build XMLRPC support 
# 
Summary:	Motion is a software motion detector
Summary(pl):	Motion - programowy wykrywacz ruchu
Name:		motion
Version:	3.1.19
Release:	0.1
Group:		Applications/Graphics
License:	GPL
Source0:	http://dl.sourceforge.net/motion/%{name}-%{version}.tar.gz
# Source0-md5:	cff1c8c56eb6b6ef8a5928780ca79cfa
URL:		http://www.lavrsen.dk/twiki/bin/view/Motion/WebHome
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	ffmpeg-devel >= 0.4.8
BuildRequires:	libjpeg-devel
%{?with_mysql:BuildRequires:    mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_xmlrpc:BuildRequires:	xmlrpc-c-devel}
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
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_examplesdir}/%{name}-%{version},%{_sysconfdir}}
install motion-dist.conf $RPM_BUILD_ROOT%{_sysconfdir}/motion.conf 
cp {motion-dist.conf,thread*,motion.init-RH}	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%makeinstall

mv $RPM_BUILD_ROOT%{_datadir}/doc doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS FAQ README README.axis_2100 motion_guide.html
%attr(755,root,root) %{_bindir}/motion
%attr(755,root,root) %{_bindir}/motion-control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/motion.conf
%{_datadir}/motion
%{_mandir}/man1/*
%{_examplesdir}/%{name}-%{version}
