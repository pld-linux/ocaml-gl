Summary:	OpenGL binding for OCaml
Summary(pl):	Wi�zania OpenGL dla OCamla
Name:		ocaml-gl
Version:	0.9
Release:	5
License:	BSD-like
Group:		Libraries
Vendor:		Nickolay Kolchin-Semyonov <snob@snob.spb.ru>
Source0:	http://dl.sourceforge.net/camlgl/ocamlgl-%{version}.tar.bz2
# Source0-md5:	d4e98e57b5717c758afabb23a357181a
Patch0:		%{name}-X11R6.patch
Patch1:		%{name}-wait_for_event.patch
Patch2:		%{name}-xlibs.patch
URL:		http://camlgl.sourceforge.net/
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
BuildRequires:	glut-devel
BuildRequires:	ocaml >= 3.07
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Binding for OpenGL up to 1.4, with NV30 and ATI extensions. Functions
names match exactly C equivalents, constants: GL_BLAH -> cgl_blah. It
is not particularly type safe, but good if already you have OpenGL
experience from other languages.

This package contains files needed to run bytecode executables using
this library.

%description -l pl
Wi�zania dla OpenGL do wersji 1.4, z rozszerzeniami NV30 oraz ATI.
Nazwy funkcji s� dok�adnie takie same jak w C, sta�e: GL_BLAH ->
cgl_blah. Wi�zanie to nie jest szczeg�lnie bezpieczne pod wzgl�dem
typ�w, ale jest dobre je�li posiadasz ju� jakie� do�wiadczenie z
OpenGL w innych j�zykach programowania.

Pakiet ten zawiera binaria potrzebne do uruchamiania program�w
u�ywaj�cych tej biblioteki.

%package devel
Summary:	OpenGL binding for OCaml - development part
Summary(pl):	Wi�zania OpenGL dla OCamla - cze�� programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
Binding for OpenGL up to 1.4, with NV30 and ATI extensions. Functions
names match exactly C equivalents, constants: GL_BLAH -> cgl_blah. It
is not particularly type safe, but good if already you have OpenGL
experience from other languages.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
Wi�zania dla OpenGL do wersji 1.4, z rozszerzeniami NV30 oraz ATI.
Nazwy funkcji s� dok�adnie takie same jak w C, sta�e: GL_BLAH ->
cgl_blah. Wi�zanie to nie jest szczeg�lnie bezpieczne pod wzgl�dem
typ�w, ale jest dobre je�li posiadasz ju� jakie� do�wiadczenie z
OpenGL w innych j�zykach programowania.

Pakiet ten zawiera pliki niezb�dne do tworzenia program�w u�ywaj�cych
tej biblioteki.

%prep
%setup -q -n ocamlgl
%patch0 -p1
%patch1 -p1
%patch2

%build
%{__make} -C gl \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC"
%{__make} -C hgl \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC"
%{__make} -C glfw \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	X11LIBS="-L/usr/X11R6/%{_lib}"
%{__make} -C glut \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	X11LIBS="-L/usr/X11R6/%{_lib}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{gl,stublibs}

install lib/*.cm[ixa]* lib/*.a $RPM_BUILD_ROOT%{_libdir}/ocaml/gl
install lib/dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlgl-gl
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlgl-gl/META <<EOF
requires = "bigarray"
version = "%{version}"
directory = "+gl"
archive(byte) = "gl.cma"
archive(native) = "gl.cmxa"
linkopts = ""
EOF

for f in glut hgl glfw ; do
	install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlgl-$f
	cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlgl-$f/META <<EOF
requires = "ocamlgl-gl"
version = "%{version}"
directory = "+gl"
archive(byte) = "$f.cma"
archive(native) = "$f.cmxa"
linkopts = ""
EOF
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc LICENSE glfw/license.txt README Announce doc/*
%dir %{_libdir}/ocaml/gl
%{_libdir}/ocaml/gl/*.cm[ixa]*
%{_libdir}/ocaml/gl/*.a
%{_libdir}/ocaml/site-lib/*
%{_examplesdir}/%{name}-%{version}
