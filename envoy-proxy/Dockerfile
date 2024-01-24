# Dockerfile for Envoy

# Use an official Envoy image as a base
FROM envoyproxy/envoy:v1.18.3

# Copy the Envoy configuration into the container
COPY envoy.yaml /etc/envoy/envoy.yaml

# Expose the port that Envoy will listen on
EXPOSE 8081

# Command to start Envoy with the specified configuration
CMD ["envoy", "-c", "/etc/envoy/envoy.yaml"]
