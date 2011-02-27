##### GENERAL STUFF #####

%define major 10
%define libname %mklibname exiv2_ %major
%define libdev %mklibname exiv2 -d

Summary:	Command line tool to access EXIF data in image files
Name:		exiv2
Version:	0.21.1
Release:	%mkrel 1
License:	GPLv2+
Group:		Graphics
Url:		http://www.exiv2.org/

##### SOURCE FILES #####

Source: http://www.exiv2.org/%name-%{version}.tar.gz

##### ADDITIONAL DEFINITIONS #####

#Provides:	libexiv
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: doxygen 
BuildRequires: graphviz
BuildRequires: python
BuildRequires: libxslt-proc
BuildRequires: expat-devel
BuildRequires: zlib-devel

##### SUB-PACKAGES #####

%description
Exiv2 is a command line utility to access image metadata:

    * print the Exif metadata of JPEG, TIFF and several RAW image 
      formats as summary info, interpreted values, or the plain data 
      for each tag (a sample is here)
    * print the IPTC metadata of JPEG images
    * print, set and delete the JPEG comment of JPEG images
    * set, add and delete Exif and IPTC metadata of JPEG images
    * adjust the Exif timestamp (that's how it all started...)
    * rename Exif image files according to the Exif timestamp
    * extract, insert and delete Exif metadata, IPTC metadata and JPEG 
      comments
    * extract, insert and delete the thumbnail image embedded in the
      Exif metadata
    * fix the Exif ISO setting of picture taken with Nikon cameras

%package -n %libname
Summary:	Library to access EXIF data in image files
#Provides:	libexiv
Group:		Graphics
Obsoletes:  %{_lib}exiv22 < 0.16-1
 
%description -n %libname
libexiv2 is a C++ library to access image metadata. libexiv2 is free
software.

The Exiv2 library provides

    * full read and write access to the Exif and IPTC metadata of
      an image through Exiv2 keys and standard C++ iterators
      (Example1, Example2, Example3, Example4)
    * a smart IPTC implementation that does not affect data that
      programs like Photoshop store in the same image segment
    * Exif MakerNote support:
          o MakerNote tags can be accessed just like any other Exif metadata
          o a sophisticated write algorithm avoids corrupting the MakerNote:
              1) the MakerNote is not re-located if possible at all, and
              2) MakerNote Ifd offsets are re-calculated if the MakerNote 
                 needs to be moved (for known Ifd MakerNotes)
    * extract and delete methods for Exif thumbnails (both, JPEG and TIFF
      thumbnails)
    * set methods for Exif thumbnails (JPEG only, TIFF thumbnails can be
      set from individual tags)
    * complete API documentation (by Doxygen)

%package -n %{libdev}
Summary: 	Headers and links to compile against the "%{libname}" library
Requires: 	%{libname} = %{version}
Requires:       multiarch-utils
Provides:	libexiv-devel = %{version}
Obsoletes: %{_lib}exiv2_2-devel
Group:		Development/C

%description -n %{libdev}
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%package doc
Summary: Exiv2 library documentation
Group: Books/Computer books
Conflicts: %{_lib}exiv2_2-devel
BuildArch: noarch

%description doc
Exiv2 library documentation.

##### PREP #####

%prep
%setup -q -n exiv2-%{version}

##### BUILD #####

%build
# "autogen" is needed if we have a CVS/SVN snapshot.
#./autogen.sh

#LDFLAGS="$LDFLAGS -module"
%configure2_5x --enable-shared
%make
%make update-po -C po
%make doc

##### INSTALL #####

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

##### PRE/POST INSTALL SCRIPTS #####

%find_lang exiv2

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT


##### FILE LISTS FOR ALL BINARY PACKAGES #####

##### exiv2
%files  -f %{name}.lang
%doc COPYING README
%{_bindir}/exiv2
%{_mandir}/man1/*

##### libexiv2
%files -n %libname
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.%{major}*

##### libexiv2-devel
%files -n %{libdev}
%defattr(-,root,root)
%{_libdir}/lib%{name}.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files doc
%defattr(-,root,root)
%doc doc/ChangeLog doc/cmd.txt doc/html doc/include doc/index.html doc/templates


##### CHANGELOG #####
