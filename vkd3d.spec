%ifarch %{x86_64}
%bcond_without compat32
%endif

%define libname %mklibname %{name} 1
%define devname %mklibname -d %{name}

%define libutils %mklibname %{name}-utils 1
%define devutils %mklibname -d %{name}-utils

%define libshader %mklibname %{name}-shader 1
%define devshader %mklibname -d %{name}-shader

%define lib32name %mklib32name %{name} 1
%define dev32name %mklib32name -d %{name}

%define lib32utils %mklib32name %{name}-utils 1
%define dev32utils %mklib32name -d %{name}-utils

%define lib32shader %mklib32name %{name}-shader 1
%define dev32shader %mklib32name -d %{name}-shader

#define date 20200702

Name:		vkd3d
Version:	1.10
Release:	%{?date:0.%{date}.}2
Summary:	D3D12 to Vulkan translation library

License:	LGPLv2+
URL:		https://source.winehq.org/git/vkd3d.git
# Interesting forks:
# https://github.com/d3d12/vkd3d
# https://github.com/ValveSoftware/vkd3d
Source0:	https://dl.winehq.org/vkd3d/source/%{name}-%{version}%{?date:-%{date}}.tar.xz

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:	pkgconfig(xcb)
BuildRequires:	spirv-headers
BuildRequires:	pkgconfig(SPIRV-Tools)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-icccm)
# For widl
BuildRequires:	mingw

%if %{with compat32}
BuildRequires:  libc6
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libvulkan)
BuildRequires:	devel(libxcb-util)
BuildRequires:	devel(libxcb-keysyms)
BuildRequires:	devel(libxcb-icccm)
BuildRequires:	libspirv-tools-devel
%endif

%description
The vkd3d project includes libraries, shaders, utilities, and demos for
translating D3D12 to Vulkan.

%package -n %{libname}
Summary:	D3D12 to Vulkan translation library

%description -n %{libname}
libvkd3d is the main component of the vkd3d project. It's a 3D graphics
library built on top of Vulkan with an API very similar to Direct3D 12.

%package -n %{devname}
Summary:	Development files for vkd3d
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for vkd3d

%package -n %{libutils}
Summary:	Utility library for vkd3d

%description -n %{libutils}
libvkd3d-utils contains simple implementations of various functions which
might be useful for source ports of Direct3D 12 applications.

%package -n %{devutils}
Summary:	Development files for libvkd3d-utils
Requires:	%{libutils} = %{EVRD}

%description -n %{devutils}
Development files for libvkd3d-utils

%package -n %{libshader}
Summary:	Shader library for vkd3d

%description -n %{libshader}
libvkd3d-shader contains shader functions for
source ports of Direct3D 12 applications.

%package -n %{devshader}
Summary:	Development files for libvkd3d-shader
Requires:	%{libshader} = %{EVRD}

%description -n %{devshader}
Development files for libvkd3d-shader

%if %{with compat32}
%package -n %{lib32name}
Summary:	D3D12 to Vulkan translation library (32-bit)

%description -n %{lib32name}
libvkd3d is the main component of the vkd3d project. It's a 3D graphics
library built on top of Vulkan with an API very similar to Direct3D 12.

%package -n %{dev32name}
Summary:	Development files for vkd3d (32-bit)
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
Development files for vkd3d

%package -n %{lib32utils}
Summary:	Utility library for vkd3d (32-bit)

%description -n %{lib32utils}
libvkd3d-utils contains simple implementations of various functions which
might be useful for source ports of Direct3D 12 applications.

%package -n %{dev32utils}
Summary:	Development files for libvkd3d-utils (32-bit)
Requires:	%{devutils} = %{EVRD}
Requires:	%{lib32utils} = %{EVRD}

%description -n %{dev32utils}
Development files for libvkd3d-utils

%package -n %{lib32shader}
Summary:	Shader library for vkd3d (32-bit)

%description -n %{lib32shader}
libvkd3d-shader contains shader functions for
source ports of Direct3D 12 applications.

%package -n %{dev32shader}
Summary:	Development files for libvkd3d-shader (32-bit)
Requires:	%{devshader} = %{EVRD}
Requires:	%{lib32shader} = %{EVRD}

%description -n %{dev32shader}
Development files for libvkd3d-shader
%endif

%prep
%autosetup -p1
[ -e configure ] || ./autogen.sh

export WIDL=x86_64-w64-mingw32-widl

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 --with-spirv-tools
cd ..
%endif
mkdir build
cd build
%configure --with-spirv-tools
cd ..

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%files -n %{libname}
%doc AUTHORS INSTALL README
%license COPYING LICENSE
%{_libdir}/libvkd3d.so.1*

%files -n %{devname}
%dir %{_includedir}/vkd3d
%{_includedir}/vkd3d/vkd3d_d3d12.h
%{_includedir}/vkd3d/vkd3d_d3d12sdklayers.h
%{_includedir}/vkd3d/vkd3d_d3dcommon.h
%{_includedir}/vkd3d/vkd3d_dxgibase.h
%{_includedir}/vkd3d/vkd3d_dxgiformat.h
%{_includedir}/vkd3d/vkd3d.h
%{_includedir}/vkd3d/vkd3d_types.h
%{_includedir}/vkd3d/vkd3d_d3d9types.h
%{_includedir}/vkd3d/vkd3d_d3dcompiler.h
%{_includedir}/vkd3d/vkd3d_d3dx9shader.h
%{_includedir}/vkd3d/vkd3d_windows.h
%{_includedir}/vkd3d/vkd3d_d3dcompiler_types.h
%{_libdir}/libvkd3d.so
%{_libdir}/pkgconfig/libvkd3d.pc

%files -n %{libutils}
%{_libdir}/libvkd3d-utils.so.1*

%files -n %{devutils}
%{_includedir}/vkd3d/vkd3d_utils.h
%{_libdir}/libvkd3d-utils.so
%{_libdir}/pkgconfig/libvkd3d-utils.pc

%files -n %{libshader}
%{_libdir}/libvkd3d-shader.so.1*

%files -n %{devshader}
%{_bindir}/vkd3d-dxbc
%{_bindir}/vkd3d-compiler
%{_includedir}/vkd3d/vkd3d_shader.h
%{_libdir}/libvkd3d-shader.so
%{_libdir}/pkgconfig/libvkd3d-shader.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libvkd3d.so.1*

%files -n %{dev32name}
%{_prefix}/lib/libvkd3d.so
%{_prefix}/lib/pkgconfig/libvkd3d.pc

%files -n %{lib32utils}
%{_prefix}/lib/libvkd3d-utils.so.1*

%files -n %{dev32utils}
%{_prefix}/lib/libvkd3d-utils.so
%{_prefix}/lib/pkgconfig/libvkd3d-utils.pc

%files -n %{lib32shader}
%{_prefix}/lib/libvkd3d-shader.so.1*

%files -n %{dev32shader}
%{_prefix}/lib/libvkd3d-shader.so
%{_prefix}/lib/pkgconfig/libvkd3d-shader.pc
%endif
