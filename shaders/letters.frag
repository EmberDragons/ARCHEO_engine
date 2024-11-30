#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec2 pixel_pos;


out vec4 fragColor;

uniform vec3 color;
uniform float hit;

uniform sampler2D u_texture_0;


void main(){
    vec3 raw_color = texture(u_texture_0, uv_0).rgb;
    raw_color+=color;
    fragColor = vec4(raw_color,1.0);
}