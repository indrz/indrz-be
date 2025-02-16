FROM docker.io/kartoza/geoserver:2.25.2
ENV GEOSERVER_LIB_DIR=$CATALINA_HOME/webapps/geoserver/WEB-INF/lib/


# Copy fonts and map icon images
COPY devops/docker/local/geoserver/fonts/*.ttf /usr/share/fonts/truetype/
COPY devops/docker/local/geoserver/fonts/ /opt/
COPY devops/docker/local/geoserver/icons/*.png /opt/geoserver/data_dir/workspaces/indrz/styles/.
COPY devops/docker/local/geoserver/icons/*.png /opt/geoserver/data_dir/styles/.

#
WORKDIR /tmp

# install java advanced imaging
RUN wget -q https://download.java.net/media/jai/builds/release/1_1_3/jai-1_1_3-lib-linux-amd64.tar.gz && \
    wget -q https://download.java.net/media/jai-imageio/builds/release/1.1/jai_imageio-1_1-lib-linux-amd64.tar.gz && \
    gunzip -c jai-1_1_3-lib-linux-amd64.tar.gz | tar xf - && \
    gunzip -c jai_imageio-1_1-lib-linux-amd64.tar.gz | tar xf - && \
    mv /tmp/jai-1_1_3/lib/*.jar $CATALINA_HOME/lib/ && \
    mv /tmp/jai-1_1_3/lib/*.so $JAVA_HOME/lib/ && \
    mv /tmp/jai_imageio-1_1/lib/*.jar $CATALINA_HOME/lib/ && \
    mv /tmp/jai_imageio-1_1/lib/*.so $JAVA_HOME/lib/ && \
    rm *tar.gz
#
## uninstall JAI default installation from geoserver to avoid classpath conflicts
## see http://docs.geoserver.org/latest/en/user/production/java.html#install-native-jai-and-imageio-extensions
##
WORKDIR $GEOSERVER_LIB_DIR
RUN rm jai_core-*jar jai_imageio-*.jar jai_codec-*.jar

# cleanup
RUN apt purge -y zip wget curl && \
    apt autoremove --purge -y && \
    rm -rf /tmp/*


RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]
