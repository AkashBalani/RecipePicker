
FROM envoyproxy/envoy:v1.18.3


COPY envoy.yaml /etc/envoy/envoy.yaml


EXPOSE 8081  
EXPOSE 8082  

CMD ["envoy", "-c", "/etc/envoy/envoy.yaml"]
