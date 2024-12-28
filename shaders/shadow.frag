#version 410

flat in vec3 fragPositionLightSpace;

out float fragDepth;

float far_plane = 100;

void main() {
    float lightDistance = length(fragPositionLightSpace);

    fragDepth = lightDistance/far_plane;
}