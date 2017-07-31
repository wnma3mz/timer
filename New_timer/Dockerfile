
########################################################## 
# Dockerfile to run a flask-based web application# Based on an centos:7 image 
##########################################################

# Set the base image to use to centos 
FROM centos:7

# Set env varibles used in this Dockerfile (add a unique prefix, such as DOCKYARD) 
# Local directory with project source 
ENV DOCKYARD_SRC=New_timer 
# Directory in Container for all project files 
ENV DOCKYARD_SRCHOME=/opt 
# Directory in container for project source files 
ENV DOCKYARD_SRCPROJ=/opt/New_timer

# Update the defualt application repository source list 
RUN yum -y install epel-release 
RUN yum -y install python-pip 
RUN yum clean all

# Copy application source code to SRCDIR 
COPY $DOCKYARD_SRC $DOCKYARD_SRCPROJ

# Create application subdirectories 
WORKDIR $DOCKYARD_SRCPROJ 
RUN mkdir log 
VOLUME [“$DOCKYARD_SRCPROJ/log/”]

# Install Python dependencies 
RUN pip install -r $DOCKYARD_SRCPROJ/requirements.txt

# Port to expose 
EXPOSE 8000

# Copy entrypoint script into the image 
WORKDIR $DOCKYARD_SRCPROJ 
ENTRYPOINT ["./start_server.sh"]

