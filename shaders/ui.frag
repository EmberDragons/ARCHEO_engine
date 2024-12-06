#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec3 v_pos;
layout (location = 4) in vec2 pixel_pos;


out vec4 fragColor;

uniform vec3 color;


void main(){

    //combining all lights, with specular and diffuse
    vec4 ui_col = vec4(color,0.0);

    fragColor = ui_col;
}