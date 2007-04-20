##### GENERAL STUFF #####

%define libname %mklibname exiv 2

Summary:	Command line tool to access EXIF data in image files
Name:		exiv2
Version:	0.14
Release:	%mkrel 1
License:	GPL
Group:		Graphics
Url:		http://www.exiv2.org/

##### SOURCE FILES #####

Source: http://www.exiv2.org/exiv2-%{version}.tar.gz

##### ADDITIONAL DEFINITIONS #####

#Provides:	libexiv
BuildRoot: %{_tmppath}/%{name}-buildroot

##### SUB-PACKAGES #####

%description

Exiv2 is a command line utility to access image metadata. Exiv2 is
free software.

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

Exiv2 is a command line utility to

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

The command line utility Exiv2 allows to

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

%package -n %{libname}-devel
Summary: 	Headers and links to compile against the "%{libname}" library
Requires: 	%{libname} = %{version}
Requires:       multiarch-utils
Provides:	libexiv-devel = %{version}
BuildRequires:  zlib1-devel
Group:		Development/C

%description -n %{libname}-devel
This package contains all files which one needs to compile programs using
the "%{libname}" library.


##### PREP #####

%prep
rm -rf $RPM_BUILD_DIR/exiv2-%{version}
%setup -q -n exiv2-%{version}



##### BUILD #####

%build
# "autogen" is needed if we have a CVS/SVN snapshot.
#./autogen.sh

#LDFLAGS="$LDFLAGS -module"
%configure --enable-shared
%make
cd po
make update-po
cd ..



##### INSTALL #####

%install
rm -rf $RPM_BUILD_ROOT

#makeinstall
%make DESTDIR=%{buildroot} install


##### PRE/POST INSTALL SCRIPTS #####

%find_lang exiv2

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

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
%{_libdir}/lib%{name}.so.*

##### libexiv2-devel
%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/lib%{name}.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
#doc doc

##### CHANGELOG #####
