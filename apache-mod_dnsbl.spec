#Module-Specific definitions
%define mod_name mod_dnsbl
%define mod_conf A30_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Blacklisting DSO for apache using DNS lookups
Name:		apache-%{mod_name}
Version:	0.10
Release:	%mkrel 5
Group:		System/Servers
License:	GPL
URL:		http://software.othello.ch/mod_dnsbl/
Source0:	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_dnsbl-0.10-compile_fix.diff
Patch1:		mod_dnsbl-apr1_fix.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	automake1.7
BuildRequires:	autoconf2.5
BuildRequires:  file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_dnsbl is a blacklisting module for the apache proxy.  It uses
the DNS as a distributed database for blacklist data. In addition
to simple block/pass decisions, it can also override
authentication or virus scanning with mod_clamav. Furthermore,
such rules can be dependent on time.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

cp %{SOURCE1} %{mod_conf}

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.7; automake-1.7 --add-missing --copy; autoconf --force

%configure2_5x \
    --with-apxs=%{_sbindir}/apxs

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

install -m0755 dnsbl_redirector %{buildroot}%{_sbindir}/
install -m0644 rules %{buildroot}%{_sysconfdir}/dnsbl_redirector.rules
install -m0644 dnsbl_redirector.8 %{buildroot}%{_mandir}/man8/

install -m0755 blacklist2zone %{buildroot}%{_sbindir}/

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README mod_dnsbl.css mod_dnsbl.html sample.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/dnsbl_redirector.rules
%attr(0755,root,root) %{_sbindir}/dnsbl_redirector
%attr(0755,root,root) %{_sbindir}/blacklist2zone
%attr(0644,root,root) %{_mandir}/man8/dnsbl_redirector.8*
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


