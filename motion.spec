Summary:	Motion is a software motion detector
Summary(pl):	Motion - programowy wykrywacz ruchu
Name:		motion
Version:	3.1.16
Release:	1
Group:		Applications/Graphics
License:	GPL
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	72beb2940d0edddd0d6856531c93c258
URL:		http://www.lavrsen.dk/twiki/bin/view/Motion/WebHome/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	ffmpeg-devel >= 0.4.8
BuildRequires:	libjpeg-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
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
chmod 755 configure
%configure \
	--with-libavcodec=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

%makeinstall

mv $RPM_BUILD_ROOT%{_datadir}/doc/ doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS FAQ README README.axis_2100 mask.pgm motion_guide.html
%attr(755,root,root) %{_bindir}/motion
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/motion-dist.conf
%{_datadir}/motion
%{_mandir}/man1/*
