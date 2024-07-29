#Using python
FROM python:3.9
# Using Layered approach for the installation of requirements
RUN mkdir /root/dtab
RUN pip install dash-bio==1.0.1
RUN pip install dash_bootstrap_components
#Copy files to your container
COPY DataTableCode-Version5.py /root/dtab/
COPY DashDataTable.csv /root/dtab/
EXPOSE 8050

CMD ["python", "/root/dtab/DataTableCode-Version5.py"]

