%define libname %mklibname %{name} 1
%define devname %mklibname -d %{name}

%define libutils %mklibname %{name}-utils 1
%define devutils %mklibname -d %{name}-utils

Name:		vkd3d
Version:	1.1
Release:	1
Summary:	D3D12 to Vulkan translation library

License:	LGPLv2+
URL:		https://source.winehq.org/git/vkd3d.git
Source0:	https://dl.winehq.org/vkd3d/source/%{name}-%{version}.tar.xz
Source1:	https://dl.winehq.org/vkd3d/source/%{name}-%{version}.tar.xz.sign

BuildRequires:	pkgconfig(xcb)
BuildRequires:	spirv-headers
BuildRequires:	pkgconfig(SPIRV-Tools)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-icccm)

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

%prep
%autosetup -p1

%build
%configure --with-spirv-tools
%make_build

%install
%make_install

%files -n %{libname}
%doc AUTHORS INSTALL README
%license COPYING LICENSE
%{_libdir}/libvkd3d.so.1*


%files -n %{devname}
%dir %{_includedir}/vkd3d
%{_includedir}/vkd3d/vkd3d_d3d12.h
%{_includedir}/vkd3d/vkd3d_d3dcommon.h
%{_includedir}/vkd3d/vkd3d_dxgibase.h
%{_includedir}/vkd3d/vkd3d_dxgiformat.h
%{_includedir}/vkd3d/vkd3d.h
%{_includedir}/vkd3d/vkd3d_windows.h
%{_libdir}/libvkd3d.so
%{_libdir}/pkgconfig/libvkd3d.pc


%files -n %{libutils}
%{_libdir}/libvkd3d-utils.so.1*


%files -n %{devutils}
%{_includedir}/vkd3d/vkd3d_utils.h
%{_libdir}/libvkd3d-utils.so
%{_libdir}/pkgconfig/libvkd3d-utils.pc
