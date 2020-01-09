Summary: A TLS protocol implementation
Name: gnutls
Version: 2.8.5
Release: 18%{?dist}
# The libgnutls library is LGPLv2+, utilities and remaining libraries are GPLv3+
License: GPLv3+ and LGPLv2+
Group: System Environment/Libraries
BuildRequires: libgcrypt-devel >= 1.2.2, gettext
BuildRequires: zlib-devel, readline-devel, libtasn1-devel
BuildRequires: lzo-devel, libtool, automake, autoconf
BuildRequires: guile-devel, texinfo
URL: http://www.gnutls.org/
#Source0: ftp://ftp.gnutls.org/pub/gnutls/%{name}-%{version}.tar.gz
#Source1: ftp://ftp.gnutls.org/pub/gnutls/%{name}-%{version}.tar.gz.sig
# XXX patent tainted SRP code removed.
Source0: %{name}-%{version}-nosrp.tar.bz2
Source1: libgnutls-config
Patch1: gnutls-2.8.5-rpath.patch
Patch3: gnutls-2.8.5-safe-renegotiation.patch
Patch4: gnutls-2.8.5-cve-2011-4128.patch
Patch5: gnutls-2.8.5-cve-2012-1573.patch
Patch6: gnutls-2.8.5-tls12-compat.patch
Patch7: gnutls-2.8.5-docfix.patch
Patch8: gnutls-2.8.5-pkcs8-fallback.patch
Patch9: gnutls-2.8.5-aliasing.patch
Patch10: gnutls-2.8.5-cve-2013-1619.patch
Patch11: gnutls-2.8.5-cve-2014-0092.patch
Patch12: gnutls-2.8.5-server-hello-fix.patch
Patch13: gnutls-2.8.5-integer-padding.patch
Patch14: gnutls-2.8.5-bz1159778.patch
Patch15: gnutls-2.8.5-mpi-print-init.patch
Patch16: gnutls-2.8.5-cve-2015-0282.patch
Patch17: gnutls-2.8.5-cve-2015-0294.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libgcrypt >= 1.2.2

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel
Requires: pkgconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%package utils
License: GPLv3+
Summary: Command line tools for TLS protocol
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%package guile
Summary: Guile bindings for the GNUTLS library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: guile

%description
GnuTLS is a project that aims to develop a library which provides a secure 
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.

%description devel
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains files needed for developing applications with
the GnuTLS library.

%description utils
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains command line TLS client and server and certificate
manipulation tools.

%description guile
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains Guile bindings for the library.

%prep
%setup -q
%patch1 -p1 -b .rpath
%patch3 -p1 -b .reneg
%patch4 -p1 -b .data-size
%patch5 -p1 -b .packet
%patch6 -p1 -b .tls12
%patch7 -p1 -b .docfix
%patch8 -p1 -b .pkcs8
%patch9 -p1 -b .aliasing
%patch10 -p1 -b .lucky13
%patch11 -p1 -b .cert-check
%patch12 -p1 -b .server-hello
%patch13 -p1 -b .integer-pad
%patch14 -p1 -b .bz1159778
%patch15 -p1 -b .mpi-init
%patch16 -p1 -b .pkcs1
%patch17 -p1 -b .algo-check

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

chmod a+x tests/safe-renegotiation/testsrn

%build
%configure --with-libtasn1-prefix=%{_prefix} \
           --with-included-libcfg \
           --disable-static \
           --disable-openssl-compatibility \
           --disable-srp-authentication
make
cp lib/COPYING COPYING.LIB

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
rm -f $RPM_BUILD_ROOT%{_bindir}/srptool
rm -f $RPM_BUILD_ROOT%{_bindir}/gnutls-srpcrypt
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-config
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-extra-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/srptool.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*srp*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libguile*.a
%find_lang libgnutls

%check
make check

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/gnutls.info.gz ]; then
    /sbin/install-info %{_infodir}/gnutls.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ $1 = 0 -a -f %{_infodir}/gnutls.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/gnutls.info.gz %{_infodir}/dir || :
fi

%post guile -p /sbin/ldconfig

%postun guile -p /sbin/ldconfig

%files -f libgnutls.lang
%defattr(-,root,root,-)
%{_libdir}/libgnutls*.so.*
%doc COPYING COPYING.LIB README AUTHORS

%files devel
%defattr(-,root,root,-)
%{_bindir}/libgnutls*-config
%{_includedir}/*
%{_libdir}/libgnutls*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/gnutls*

%files utils
%defattr(-,root,root,-)
%{_bindir}/certtool
%{_bindir}/psktool
%{_bindir}/gnutls*
%{_mandir}/man1/*
%doc doc/certtool.cfg

%files guile
%defattr(-,root,root,-)
%{_libdir}/libguile*.so*
%{_datadir}/guile/site/gnutls
%{_datadir}/guile/site/gnutls.scm

%changelog
* Tue Mar  3 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 2.8.5-18
- fix CVE-2015-0282 (#1198159)
- fix CVE-2015-0294 (#1198159)

* Thu Jan 29 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 2.8.5-17
- Corrected value initialization in mpi printing (#1129241)

* Fri Jan 16 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 2.8.5-16
- Check for expiry information in the CA certificates (#1159778)

* Tue Dec  2 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 2.8.5-15
- fix issue with integer padding in certificates and keys (#1036385)

* Wed May 28 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 2.8.5-14
- fix session ID length check (#1102025)

* Wed Feb 26 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 2.8.5-13
- fix CVE-2014-0092 (#1069891)

* Mon May 27 2013 Tomas Mraz <tmraz@redhat.com> 2.8.5-12
- fix CVE-2013-2116 - fix DoS regression in CVE-2013-1619
  upstream patch (#966754)

* Thu Feb 21 2013 Tomas Mraz <tmraz@redhat.com> 2.8.5-11
- fix CVE-2013-1619 - fix TLS-CBC timing attack (#908238)

* Mon Oct 29 2012 Tomas Mraz <tmraz@redhat.com> 2.8.5-10
- fix the build of the info manual

* Wed Oct 10 2012 Tomas Mraz <tmraz@redhat.com> 2.8.5-9
- documentation fixes in gnutls_priority_init(3), gnutls-serv(1),
  and gnutls-cli-debug(1) manual pages (#648297, #807746)
- add fallback to import the private keys as PKCS#8 (#745242)
- silence the strict aliasing warnings

* Thu May  3 2012 Tomas Mraz <tmraz@redhat.com> 2.8.5-7
- more TLS-1.2 compatibility fixes (TLS-1.2 stays disabled by default)

* Wed Mar 21 2012 Tomas Mraz <tmraz@redhat.com> 2.8.5-5
- fix CVE-2012-1573 - security issue in packet parsing (#805432)
- fix CVE-2011-4128 - buffer overflow in gnutls_session_get_data() (#752308)
- TLS-1.2 certificate request compatibility fix

* Wed Jun  2 2010 Tomas Mraz <tmraz@redhat.com> 2.8.5-4
- add support for safe renegotiation CVE-2009-3555 (#533125)

* Thu Jan 28 2010 Tomas Mraz <tmraz@redhat.com> 2.8.5-3
- drop superfluous rpath from binaries
- do not call autoreconf during build
- specify the license on utils subpackage
- do not create static libraries (#556052)

* Fri Dec 18 2009 Tomas Mraz <tmraz@redhat.com> 2.8.5-2
- disable experimental openssl compatibility code (#460310)

* Thu Dec 03 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.8.5-1.1
- Rebuilt for RHEL 6

* Mon Nov  2 2009 Tomas Mraz <tmraz@redhat.com> 2.8.5-1
- upgrade to a new upstream version

* Wed Sep 23 2009 Tomas Mraz <tmraz@redhat.com> 2.8.4-1
- upgrade to a new upstream version

* Fri Aug 14 2009 Tomas Mraz <tmraz@redhat.com> 2.8.3-1
- upgrade to a new upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Tomas Mraz <tmraz@redhat.com> 2.8.1-1
- upgrade to a new upstream version

* Wed Jun  3 2009 Tomas Mraz <tmraz@redhat.com> 2.8.0-1
- upgrade to a new upstream version

* Mon May  4 2009 Tomas Mraz <tmraz@redhat.com> 2.6.6-1
- upgrade to a new upstream version - security fixes

* Tue Apr 14 2009 Tomas Mraz <tmraz@redhat.com> 2.6.5-1
- upgrade to a new upstream version, minor bugfixes only

* Fri Mar  6 2009 Tomas Mraz <tmraz@redhat.com> 2.6.4-1
- upgrade to a new upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Tomas Mraz <tmraz@redhat.com> 2.6.3-1
- upgrade to a new upstream version

* Thu Dec  4 2008 Tomas Mraz <tmraz@redhat.com> 2.6.2-1
- upgrade to a new upstream version

* Tue Nov 11 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-3
- fix chain verification issue CVE-2008-4989 (#470079)

* Thu Sep 25 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-2
- add guile subpackage (#463735)
- force new libtool through autoreconf to drop unnecessary rpaths

* Tue Sep 23 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-1
- new upstream version

* Tue Jul  1 2008 Tomas Mraz <tmraz@redhat.com> 2.4.1-1
- new upstream version
- correct the license tag
- explicit --with-included-opencdk not needed
- use external lzo library, internal not included anymore

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> 2.4.0-1
- upgrade to latest upstream

* Tue May 20 2008 Tomas Mraz <tmraz@redhat.com> 2.0.4-3
- fix three security issues in gnutls handshake - GNUTLS-SA-2008-1
  (#447461, #447462, #447463)

* Mon Feb  4 2008 Joe Orton <jorton@redhat.com> 2.0.4-2
- use system libtasn1

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> 2.0.4-1
- upgrade to latest upstream

* Tue Aug 21 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-2
- license tag fix

* Wed Jun  6 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-1
- upgrade to latest upstream (#232445)

* Tue Apr 10 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-2
- properly require install-info (patch by Ville Skyttä)
- standard buildroot and use dist tag
- add COPYING and README to doc

* Wed Feb  7 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-1
- new upstream version
- drop libtermcap-devel from buildrequires

* Thu Sep 14 2006 Tomas Mraz <tmraz@redhat.com> 1.4.1-2
- detect forged signatures - CVE-2006-4790 (#206411), patch
  from upstream

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.1-1
- upgrade to new upstream version, only minor changes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.0-1.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.0-1
- upgrade to new upstream version (#192070), rebuild
  of dependent packages required

* Tue May 16 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-2
- added missing buildrequires

* Mon Feb 13 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-1
- updated to new version (fixes CVE-2006-0645)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.9-3
- rebuilt

* Fri Dec  9 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-2
- replaced *-config scripts with calls to pkg-config to
  solve multilib conflicts

* Wed Nov 23 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-1
- upgrade to newest upstream
- removed .la files (#172635)

* Sun Aug  7 2005 Tomas Mraz <tmraz@redhat.com> 1.2.6-1
- upgrade to newest upstream (rebuild of dependencies necessary)

* Mon Jul  4 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-2
- split the command line tools to utils subpackage

* Sat Apr 30 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-1
- new upstream version fixes potential DOS attack

* Sat Apr 23 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-2
- readd the version script dropped by upstream

* Fri Apr 22 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-1
- update to the latest upstream version on the 1.0 branch

* Wed Mar  2 2005 Warren Togami <wtogami@redhat.com> 1.0.20-6
- gcc4 rebuild

* Tue Jan  4 2005 Ivana Varekova <varekova@redhat.com> 1.0.20-5
- add gnutls Requires zlib-devel (#144069)

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 1.0.20-4
- Make gnutls-devel Require libgcrypt-devel

* Tue Sep 21 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-3
- rebuild with release++, otherwise unchanged.

* Tue Sep  7 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-2
- patent tainted SRP code removed.

* Sun Sep  5 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-1
- update to 1.0.20.
- add --with-included-opencdk --with-included-libtasn1
- add --with-included-libcfg --with-included-lzo
- add --disable-srp-authentication.
- do "make check" after build.

* Fri Mar 21 2003 Jeff Johnson <jbj@redhat.com> 0.9.2-1
- upgrade to 0.9.2

* Tue Jun 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.4-1
- update to 0.4.4.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- update to 0.4.3.

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com> 0.4.2-1
- update to 0.4.2.
- change license to LGPL.
- include splint annotations patch.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.4.0-1
- update to 0.4.0

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-1
- update to 0.3.2

* Wed Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.0-1
- add a URL

* Wed Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
