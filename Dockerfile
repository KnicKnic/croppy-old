
# Pull base image
FROM oldy


COPY ./ /data/
COPY policy.xml  /etc/ImageMagick-6/policy.xml

# Define working directory
 WORKDIR /data

# Define default command
CMD ["python3", "flask_prog.py"]
