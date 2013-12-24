#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	MonadCatchIO-transformers
Summary:	Monad-transformer compatible version of the Control.Exception module
Summary(pl.UTF-8):	Wersja modułu Control.Exception zgodna z transformatorami monad
Name:		ghc-%{pkgname}
Version:	0.3.1.0
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/MonadCatchIO-transformers
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	3b54254de4a192fdbdea06d2950cac8d
URL:		http://hackage.haskell.org/package/MonadCatchIO-transformers
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base < 4.8
BuildRequires:	ghc-extensible-exceptions >= 0.1
BuildRequires:	ghc-extensible-exceptions < 0.2
BuildRequires:	ghc-monads-tf >= 0.1
BuildRequires:	ghc-monads-tf < 0.2
BuildRequires:	ghc-transformers >= 0.2
BuildRequires:	ghc-transformers < 0.4
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof < 4.8
BuildRequires:	ghc-extensible-exceptions-prof >= 0.1
BuildRequires:	ghc-extensible-exceptions-prof < 0.2
BuildRequires:	ghc-monads-tf-prof >= 0.1
BuildRequires:	ghc-monads-tf-prof < 0.2
BuildRequires:	ghc-transformers-prof >= 0.2
BuildRequires:	ghc-transformers-prof < 0.4
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base < 4.8
Requires:	ghc-extensible-exceptions >= 0.1
Requires:	ghc-extensible-exceptions < 0.2
Requires:	ghc-monads-tf >= 0.1
Requires:	ghc-monads-tf < 0.2
Requires:	ghc-transformers >= 0.2
Requires:	ghc-transformers < 0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Provides functions to throw and catch exceptions. Unlike the functions
from Control.Exception, which work in IO, these work in any stack of
monad transformers (from the transformers package) with IO as the base
monad. You can extend this functionality to other monads, by creating
an instance of the MonadCatchIO class.

%description -l pl.UTF-8
Ten pakiet dostarcza funkcje do rzucania i przechwytywania wyjątków. W
przeciwieństwie do funkcji z Control.Exceptions, działających w IO, te
działają w dowolnym stosie transformatorów monad (z pakietu
transformers) z IO jako podstawową monadą. Można rozszerzać tę
funkcjonalność na inne monady poprzez tworzenie instancji klasy
MonadCatchIO.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof < 4.8
Requires:	ghc-extensible-exceptions-prof >= 0.1
Requires:	ghc-extensible-exceptions-prof < 0.2
Requires:	ghc-monads-tf-prof >= 0.1
Requires:	ghc-monads-tf-prof < 0.2
Requires:	ghc-transformers-prof >= 0.2
Requires:	ghc-transformers-prof < 0.4

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSMonadCatchIO-transformers-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSMonadCatchIO-transformers-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/CatchIO.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/CatchIO
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/CatchIO/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSMonadCatchIO-transformers-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/CatchIO.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/CatchIO/*.p_hi
