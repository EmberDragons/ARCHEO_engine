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
float dist_center = 0.05;

void main(){

    //combining all lights, with specular and diffuse
    vec3 shading = vec3(1,1,1);

    //converting it to color with 255 as max
    vec3 color = texture(u_texture_0, uv_0).rgb;
    
    //gamma correction
    float gamma = 2.2;
    color=pow(color, vec3(gamma));
    color=pow(color, vec3(1/gamma));

    //crosshair
    if (sqrt(pow(pixel_pos.x-center.x,2)+pow(pixel_pos.y-center.y,2))<dist_center) {
        color = vec3(0.0);
    }

    fragColor = vec4(color, 1.0);
}