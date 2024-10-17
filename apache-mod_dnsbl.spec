#Module-Specific definitions
%define mod_name mod_dnsbl
%define mod_conf A30_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Blacklisting DSO for apache using DNS lookups
Name:		apache-%{mod_name}
Version:	0.11
Release:	9
Group:		System/Servers
License:	GPL
URL:		https://software.othello.ch/mod_dnsbl/
Source0:	http://software.othello.ch/mod_dnsbl/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	automake
BuildRequires:	autoconf2.5
BuildRequires:  file
Epoch:		1

%description
mod_dnsbl is a blacklisting module for the apache proxy.  It uses
the DNS as a distributed database for blacklist data. In addition
to simple block/pass decisions, it can also override
authentication or virus scanning with mod_clamav. Furthermore,
such rules can be dependent on time.

%prep

%setup -q -n %{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

cp %{SOURCE1} %{mod_conf}

%build

%configure2_5x --localstatedir=/var/lib \
    --with-apxs=%{_bindir}/apxs

%make

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -m0755 dnsbl_redirector %{buildroot}%{_sbindir}/
install -m0644 rules %{buildroot}%{_sysconfdir}/dnsbl_redirector.rules
install -m0644 dnsbl_redirector.8 %{buildroot}%{_mandir}/man8/
install -m0755 contrib/blacklist2zone %{buildroot}%{_sbindir}/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc AUTHORS ChangeLog INSTALL NEWS README mod_dnsbl.css mod_dnsbl.html contrib/sample.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/dnsbl_redirector.rules
%attr(0755,root,root) %{_sbindir}/dnsbl_redirector
%attr(0755,root,root) %{_sbindir}/blacklist2zone
%attr(0644,root,root) %{_mandir}/man8/dnsbl_redirector.8*
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-9mdv2011.0
+ Revision: 678305
- mass rebuild

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-8mdv2011.0
+ Revision: 627729
- don't force the usage of automake1.7

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-7mdv2011.0
+ Revision: 587963
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-6mdv2010.1
+ Revision: 516091
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-5mdv2010.0
+ Revision: 406575
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-4mdv2009.1
+ Revision: 325694
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-3mdv2009.0
+ Revision: 234931
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-2mdv2009.0
+ Revision: 215570
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Sat May 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-1mdv2009.0
+ Revision: 205384
- 0.11
- drop obsolete patches

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-5mdv2008.1
+ Revision: 181719
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.10-4mdv2008.1
+ Revision: 170718
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-3mdv2008.0
+ Revision: 82555
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10-2mdv2007.1
+ Revision: 140667
- rebuild

* Tue Jan 02 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-1mdv2007.1
+ Revision: 103365
- bunzip patches and sources
- fix apr1/apache22 build (P0,P1)
- Import apache-mod_dnsbl

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.10-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.10-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.10-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.10-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.10-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.10-1mdk
- rebuilt for apache 2.0.53

* Fri Nov 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.10-1mdk
- initial mandrake package

