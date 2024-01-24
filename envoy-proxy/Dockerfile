
FROM envoyproxy/envoy:v1.18.3


COPY envoy.yaml /etc/envoy/envoy.yaml


EXPOSE 4201  
EXPOSE 8001  

CMD ["envoy", "-c", "/etc/envoy/envoy.yaml"]
