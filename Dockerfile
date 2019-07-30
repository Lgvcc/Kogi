FROM centos:centos7
MAINTAINER The Weather Spider Project <richie.min@epmap.org>


ENV LANG en_US.UTF-8
RUN rpm -ivh https://mirrors.aliyun.com/centos/7/os/x86_64/Packages/wget-1.14-18.el7.x86_64.rpm  && \
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && \
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo

RUN yum -y update; yum clean all && \
yum -y install epel-release; yum clean all && \
yum -y install python-pip && \
yum -y install gcc

WORKDIR /opt

RUN wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
RUN tar -zxvf Python-3.6.5.tgz

RUN  yum -y install zlib* && \
yum -y install make && \
yum -y install openssl && \
yum -y install openssl-devel && \
/opt/Python-3.6.5/configure --prefix=/usr/local/python3.6

RUN mkdir -p /src && \
make && \
make install

WORKDIR /src
COPY . /src


RUN wget https://raw.githubusercontent.com/emmetio/pyv8-binaries/master/pyv8-linux64-p3.zip && \
yum -y install unzip

RUN ln -s /usr/local/python3.6/bin/python3 /usr/bin/python3 && \
ln -s /usr/local/python3.6/bin/pip3 /usr/bin/pip3 && \



RUN pip install -i https://pypi.douban.com/simple  --upgrade pip
RUN pip install -i https://pypi.douban.com/simple -r requirements.txt && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime


