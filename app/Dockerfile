#Using python
FROM python:3.9
# Using Layered approach for the installation of requirements
RUN mkdir /root/test
RUN pip install dash-bio==1.0.1
RUN pip install dash_bootstrap_components
#Copy files to your container
COPY DataTableCode-Version2.py /root/test/
EXPOSE 8050

CMD ["python", "/root/test/DataTableCode-Version2.py"]

