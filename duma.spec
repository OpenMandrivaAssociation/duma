# $Id$
# Authority: dries
# Upstream:  Hayati Ayguen <h_ayguen$web,de>

%define real_version 2_5_15

Summary:	Detect Unintended Memory Access
Name:		duma
Version:	2.5.15
Release:	2
License:	GPL
Group:		Development/Other
URL:		http://duma.sourceforge.net/

Source:		http://dl.sf.net/duma/duma_%{real_version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	gcc-c++

%description
DUMA (Detect Unintended Memory Access) stops your program on the exact
instruction that overruns (or underruns) a malloc() memory buffer. GDB
will then display the source-code line that causes the bug. It works by
using the virtual-memory hardware to create a red-zone at the border of
each buffer: touch that, and your program stops. It can catch formerly
impossible-to-catch overrun bugs. DUMA is a fork of Bruce Perens'
Electric Fence library.

%package devel
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n duma_%{real_version}
# disable 'testoperators' because it doesn't stop
%{__perl} -pi.orig -e "s|..CURPATH.testoperators..EXEPOSTFIX.||g;" Makefile

%build
# duma doesn't build with _smp_mflags
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_bindir}
%{__install} -d -m0755 %{buildroot}%{_mandir}/man3/
%{__install} -d -m0755 %{buildroot}%{_libdir}
%makeinstall BIN_INSTALL_DIR="%{buildroot}%{_bindir}" \
    LIB_INSTALL_DIR="%{buildroot}%{_libdir}" \
    MAN_INSTALL_DIR="%{buildroot}%{_mandir}/man3/"

rm -r %{buildroot}/%{_libdir}/libduma.a
rm -r %{buildroot}/%{_docdir}/duma/README.txt
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc INSTALL TODO README.txt
%doc %{_mandir}/man3/duma.3*
%{_bindir}/duma
%{_libdir}/libduma.so.*
#% exclude % {_docdir}/duma/README.txt

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/duma*.h
%{_includedir}/noduma.h
#% exclude % {_libdir}/libduma.a
%{_libdir}/libduma.so


%changelog
* Tue Nov 01 2011 Alexander Khrukin <akhrukin@mandriva.org> 2.5.15-1mdv2011.0
+ Revision: 709721
- build fixes with not needed files like README.txt and .a
- rpmlint fixes
- imported package duma

