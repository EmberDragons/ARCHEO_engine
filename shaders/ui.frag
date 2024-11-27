#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec3 v_pos;
layout (location = 4) in vec2 pixel_pos;


out vec4 fragColor;

uniform sampler2D u_texture_0;

//matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

//crosshair param
vec2 center = vec2(0,0);
float dist_center = 0.004;

void main(){

    //combining all lights, with specular and diffuse
    vec4 color = vec4(0.0);

    //crosshair
    if (sqrt(pow(pixel_pos.x-center.x,2)+pow(pixel_pos.y-center.y,2))<dist_center) {
        color = vec4(1.0);
    }

    fragColor = color;
}