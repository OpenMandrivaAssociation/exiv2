%define _disable_lto 1

%define major %(echo %{version} |cut -d. -f2)
%define libname %mklibname exiv2
%define devname %mklibname exiv2 -d

Summary:	Command line tool to access EXIF data in image files
Name:		exiv2
Version:	0.28.5
Release:	1
License:	GPLv2+
Group:		Graphics
Url:		https://www.exiv2.org/
#Source0:	http://www.exiv2.org/builds/%{name}-%{version}-Source.tar.gz
Source0:	https://github.com/Exiv2/exiv2/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	doxygen 
BuildRequires:	graphviz
BuildRequires:	python
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(inih)
BuildRequires:	pkgconfig(INIReader)
BuildRequires:	pkgconfig(libbrotlidec)
BuildRequires:	gettext-devel
BuildRequires:	cmake ninja

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

%package -n %{libname}
Summary:	Library to access EXIF data in image files
Group:		Graphics
 
%description -n %{libname}
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

%package -n %{devname}
Summary:	Headers and links to compile against the "%{libname}" library
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	pkgconfig(libcurl)
Requires:	pkgconfig(libssh)
Provides:	%{name}-devel = %{version}

%description -n %{devname}
This package contains all files which one needs to compile programs using
the "%{libname}" library.

%package doc
Summary:	Exiv2 library documentation
Group:		Books/Computer books
BuildArch:	noarch

%description doc
Exiv2 library documentation.

%prep
%autosetup -p1 -n %{name}-%{version}
# EXIV2_ENABLE_SSH is deprecated and requires the old unsafe libssh v1
%cmake \
	-DEXIV2_BUILD_DOC:BOOL=ON \
	-DEXIV2_ENABLE_NLS:BOOL=ON \
	-DEXIV2_ENABLE_CURL:BOOL=ON \
	-DEXIV2_ENABLE_SSH:BOOL=OFF \
	-DEXIV2_ENABLE_VIDEO:BOOL=ON \
	-DEXIV2_ENABLE_WEBREADY:BOOL=ON \
	-DEXIV2_ENABLE_XMP:BOOL=ON \
        -DEXIV2_ENABLE_BMFF:BOOL=ON \
	-DEXIV2_BUILD_SAMPLES:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build
%ninja_build -C build doc

%install
%ninja_install -C build

# to avoid unstripped-binary-or-object
chmod 0755 %{buildroot}%{_libdir}/lib%{name}.so.%{major}*

# No need to package tests
rm -f \
	%{buildroot}%{_bindir}/*-test \
	%{buildroot}%{_mandir}/man1/*-test.1*

# And no need to package the static XMP lib that's linked into
# libexiv2
rm -f \
	%{buildroot}%{_libdir}/libexiv2-xmp.a

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/exiv2
%{_bindir}/addmoddel
%{_bindir}/exifcomment
%{_bindir}/exifdata
%{_bindir}/exifprint
%{_bindir}/exifvalue
%{_bindir}/geotag
%{_bindir}/iptceasy
%{_bindir}/iptcprint
%{_bindir}/metacopy
%{_bindir}/mrwthumb
%{_bindir}/taglist
%{_bindir}/xmpdump
%{_bindir}/xmpparse
%{_bindir}/xmpprint
%{_bindir}/xmpsample
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%{_libdir}/lib%{name}.so.0*

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/exiv2/
%{_includedir}/*

%files doc
%doc %{_docdir}/exiv2
