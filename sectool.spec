Summary:	A security audit system and intrusion detection system
Name:		sectool
Version:	0.9.3
Release:	%mkrel 4
URL:		https://hosted.fedoraproject.org/sectool/wiki/WikiStart
Source0:	%{name}-%{version}.tar.bz2
Source1:	sectool.log
Patch0:		sectool-0.9.3-rpm5.patch
Patch1:		sectool-0.9.3-proper-cppflags-libs-in-makefiel.patch
License:	GPLv2+
Group:		System/Base
Requires:	gettext coreutils python python-selinux
BuildRequires:	desktop-file-utils gettext intltool asciidoc librpm-devel selinux-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%package	gui
Summary:	GUI for sectool - security audit system and intrusion detection system
License:	GPLv2+
Group:		System/Base
Requires:	sectool = %{version}-%{release}
Requires:	pygtk2 usermode

%description
sectool is a security tool that can be used both as a security audit
and intrusion detection system. It consists of set of tests, library
and command line interface tool. Tests are sorted into groups and security
levels. Admins can run certain tests, groups or whole security levels.
The library and the tools are implemented in python and tests are
language independent.

%description	gui
sectool-gui provides a GTK-based graphical user interface to sectool.

%prep
%setup -q
%patch0 -p1 -b .rpm5~
%patch1 -p1 -b .cppflags_libs~

%build
%make CFLAGS="%{optflags} -ffast-math" LDFLAGS="%{ldflags}"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
desktop-file-install --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --vendor=fedora \
   $RPM_BUILD_ROOT%{_datadir}/applications/sectool.desktop

#logrotate
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sectool
#adjust paths in sectool.conf
sed -i 's,DSC_DIR=\(.*\),DSC_DIR=%{_sysconfdir}/sectool/tests,' $RPM_BUILD_ROOT%{_sysconfdir}/sectool/sectool.conf
sed -i 's,TESTS_DIRS=\(.*\),TESTS_DIRS=%{_datadir}/sectool/tests,' $RPM_BUILD_ROOT%{_sysconfdir}/sectool/sectool.conf
sed -i 's,TDATA_DIR_BASE=\(.*\),TDATA_DIR_BASE=%{_localstatedir}/lib/sectool,' $RPM_BUILD_ROOT%{_sysconfdir}/sectool/sectool.conf
#adjust icons path in guiOutput.py
sed -i 's,__ico_path = \(.*\),__ico_path = "%{_datadir}/pixmaps/sectool/",' $RPM_BUILD_ROOT%{_datadir}/sectool/guiOutput.py
#this file is just for development
rm $RPM_BUILD_ROOT/%{_datadir}/sectool/scheduler/selftest.py

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING AUTHORS README doc/tests_documentation.html
%config(noreplace) %{_sysconfdir}/sectool/
%config(noreplace) %{_sysconfdir}/logrotate.d/sectool
%dir %{_localstatedir}/lib/sectool
%dir %{_datadir}/sectool
%{_sbindir}/sectool
#library with tests
%{_datadir}/sectool/scheduler
%{_datadir}/sectool/tests
# command line tool
%{_datadir}/sectool/actions.py*
%{_datadir}/sectool/__init__.py*
%{_datadir}/sectool/output.py*
%{_datadir}/sectool/mailoutput.py*
%{_datadir}/sectool/sectool.py*
%{_datadir}/sectool/tuierrors.py*
%{_mandir}/man8/sectool.8.*


%files gui
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/sectool-gui
%config(noreplace) %{_sysconfdir}/security/console.apps/sectool-gui
%{_bindir}/sectool-gui
%{_datadir}/sectool/gui*.py*
%{_datadir}/sectool/sectool-gui.py*
%{_datadir}/pixmaps/sectool-gui.png
%{_datadir}/pixmaps/sectool-min.png
%{_datadir}/applications/fedora-sectool.desktop
%{_datadir}/pixmaps/sectool/*.png
