
%define name	motion
%define	version 3.0.5
%define release	0.1

Summary:	Motion is a software motion detector.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Applications/Graphics
License:	GPL
Source0:	http://motion.sourceforge.net/download/%{name}-%{version}.tar.bz2
URL:		http://motion.technolust.cx/
BuildRequires:  libjpeg-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  mysql-devel
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Patch0:		motion-wrongincludepath.patch.bz2 

%description
Motion is a software motion detector. It grabs images from video4linux
devices and/or from webcams (such as the axis network cameras). Motion
is the perfect tool for keeping an eye on your property keeping only
those images that are interesting.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

#%makeinstall

mv $RPM_BUILD_ROOT%{_prefix}/doc/%{name}-%{version} doc
mv $RPM_BUILD_ROOT%{_prefix}/examples/%{name}-%{version} $RPM_BUILD_ROOT/%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG COPYING CREDITS FAQ README README.axis_2100 mask.pgm  motion_guide.html
%config(noreplace) %{_sysconfdir}/motion.conf
%{_datadir}/motion
%attr(755,root,root) %{_bindir}/motion
%{_mandir}/man1/motion.1*
