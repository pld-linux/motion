Summary:	Motion is a software motion detector
Summary(pl):	Motion - programowy wykrywacz ruchu
Name:		motion
Version:	3.0.6
Release:	1
Group:		Applications/Graphics
License:	GPL
Source0:	http://motion.sourceforge.net/download/%{name}-%{version}.tar.gz
# Source0-md5:	aa1ce10036ef34b1bd3c42d37831b54b
Patch0:		%{name}-wrongincludepath.patch.bz2
Patch1:		%{name}-ffmpeg.patch
URL:		http://motion.technolust.cx/
BuildRequires:	autoconf
BuildRequires:	curl-devel
BuildRequires:	ffmpeg-devel
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
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-libavcodec=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

mv $RPM_BUILD_ROOT%{_prefix}/doc/%{name}-%{version} doc
mv $RPM_BUILD_ROOT%{_prefix}/examples/%{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS FAQ README README.axis_2100 mask.pgm  motion_guide.html
%attr(755,root,root) %{_bindir}/motion
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/motion.conf
%{_datadir}/motion
%{_mandir}/man1/motion.1*
