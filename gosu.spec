# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: gosu
Epoch: 100
Version: 1.13
Release: 1%{?dist}
Summary: Simple Go-based setuid+setgid+setgroups+exec
License: Apache-2.0
URL: https://github.com/tianon/gosu/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.19
BuildRequires: glibc-static

%description
This is a simple tool grown out of the simple fact that su and sudo have
very strange and often annoying TTY and signal-forwarding behavior.
They're also somewhat complex to setup and use (especially in the case
of sudo), which allows for a great deal of expressivity, but falls flat
if all you need is "run this specific application as this specific user
and get out of the pipeline".

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p sbin
set -ex && \
    export CGO_ENABLED=0 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w -extldflags '-static -lm'" \
        -o ./sbin/gosu .

%install
install -Dpm755 -d %{buildroot}%{_sbindir}
install -Dpm755 -t %{buildroot}%{_sbindir}/ sbin/gosu

%files
%license LICENSE
%{_sbindir}/*

%changelog
