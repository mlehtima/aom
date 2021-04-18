# Force out of source build
%undefine __cmake_in_source_build

Name:       aom
Version:    3.12.0
Release:    1
Summary:    Royalty-free next-generation video format

License:    BSD
URL:        http://aomedia.org/
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  perl
BuildRequires:  perl(Getopt::Long)
BuildRequires:  python3-devel
%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

Provides:       av1 = %{version}-%{release}
Requires:       libaom%{?_isa} = %{version}-%{release}

%description
The Alliance for Open Media’s focus is to deliver a next-generation
video format that is:

 - Interoperable and open;
 - Optimized for the Internet;
 - Scalable to any modern device at any bandwidth;
 - Designed with a low computational footprint and optimized for hardware;
 - Capable of consistent, highest-quality, real-time video delivery; and
 - Flexible for both commercial and non-commercial content, including
   user-generated content.

This package contains the reference encoder and decoder.

%package -n libaom
Summary:        Library files for aom

%description -n libaom
Library files for aom, the royalty-free next-generation
video format.

%package -n libaom-devel
Summary:        Development files for aom
Requires:       libaom%{?_isa} = %{version}-%{release}

%description -n libaom-devel
Development files for aom, the royalty-free next-generation
video format.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}
# Set GIT revision in version
#sed -i 's@set(aom_version "")@set(aom_version "%{aom_version}")@' build/cmake/version.cmake

%build
%cmake \
       -DENABLE_CCACHE=1 \
       -DCMAKE_SKIP_RPATH=1 \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCONFIG_WEBM_IO=1 \
       -DENABLE_DOCS=0 \
       -DENABLE_NEON_I8MM=0 \
       -DENABLE_TESTS=0 \
       -DCONFIG_ANALYZER=0 \
       -DCONFIG_SHARED=1 \
       %{nil}
%cmake_build

%install
%cmake_install
rm -rf %{buildroot}%{_libdir}/libaom.a

%post -n libaom -p /sbin/ldconfig
%postun -n libaom -p /sbin/ldconfig

%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE PATENTS
%{_bindir}/aomdec
%{_bindir}/aomenc

%files -n libaom
%license LICENSE PATENTS
%{_libdir}/libaom.so.*

%files -n libaom-devel
%{_includedir}/%{name}
%{_libdir}/libaom.so
%{_libdir}/pkgconfig/%{name}.pc
