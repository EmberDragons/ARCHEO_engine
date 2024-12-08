#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec2 pixel_pos;


out vec4 fragColor;

uniform vec3 color;
uniform sampler2D u_texture_0;


void main(){

    //combining all lights, with specular and diffuse
    vec3 raw_color = texture(u_texture_0, uv_0).rgb;
    float r = raw_color.r/255;
    float g = raw_color.g/255;
    float b = raw_color.b/255;
    vec3 color_tex = vec3(r*color.r,g*color.g,b*color.b)*255;
    vec4 ui_col = vec4(color_tex,0.0);

    fragColor = ui_col;
}