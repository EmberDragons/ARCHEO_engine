#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec3 shading;

out vec4 fragColor;

uniform sampler2D u_texture_0;

void main(){

    vec3 raw_color = texture(u_texture_0, uv_0).rgb;
    float r = raw_color.r/255;
    float g = raw_color.g/255;
    float b = raw_color.b/255;
    vec3 color = vec3(r*shading.r,g*shading.g,b*shading.b)*255;
    fragColor = vec4(color, 1.0);
}