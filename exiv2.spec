%define major 26
%define libname %mklibname exiv2_ %{major}
%define devname %mklibname exiv2 -d

# FIXME -- error at link time with LTO enabled (clang 7.0-333395, binutils 2.30, exiv2 0.26):
# /tmp/lto-llvm-8c3831.o:ld-temp.o:(anonymous namespace)::registry: error: undefined reference to 'Exiv2::newPngInstance(std::auto_ptr<Exiv2::BasicIo>, bool)'
# /tmp/lto-llvm-8c3831.o:ld-temp.o:(anonymous namespace)::registry: error: undefined reference to 'Exiv2::isPngType(Exiv2::BasicIo&, bool)'

#define _disable_lto 1

Summary:	Command line tool to access EXIF data in image files
Name:		exiv2
Version:	0.26
Release:	4
License:	GPLv2+
Group:		Graphics
Url:		http://www.exiv2.org/
Source0:	http://www.exiv2.org/builds/%{name}-%{version}-trunk.tar.gz
Patch0:		exiv2-0.26-buildsystem-fixes.patch

BuildRequires:	doxygen 
BuildRequires:	graphviz
BuildRequires:	python
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	autoconf-archive
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gettext-devel

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
%autosetup -p1 -n %{name}-trunk
cd config
cp -f %{_datadir}/libtool/config/* .
aclocal
autoconf
cp -f configure ..

%build
%configure \
	--enable-shared \
	--enable-video \
	--enable-webready
%make
%make update-po -C po
%make doc -k ||:

%install
%makeinstall_std MKINSTALLDIRS=%{_datadir}/automake-*/mkinstalldirs

%find_lang exiv2

# to avoid unstripped-binary-or-object
chmod 0755 %{buildroot}%{_libdir}/lib%{name}.so.%{major}*

%files  -f %{name}.lang
%doc COPYING README
%{_bindir}/exiv2
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files doc
%doc doc/ChangeLog doc/cmd.txt doc/html doc/include doc/index.html

