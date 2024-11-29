#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec3 v_pos;
layout (location = 4) in vec2 pixel_pos;


out vec4 fragColor;

uniform vec3 color;
uniform float hit;

//crosshair param
vec2 center = vec2(0,0);
float dist_center = 0.004;

void main(){

    //combining all lights, with specular and diffuse
    vec4 ui_col = vec4(color,0.0);
    if (hit==1.0){
        ui_col = vec4(1.0,1.0,1.0,0.0);
    }
    //crosshair
    //if (sqrt(pow(pixel_pos.x-center.x,2)+pow(pixel_pos.y-center.y,2))<dist_center) {
    //    ui_col = vec4(color,1.0);
    //}

    fragColor = ui_col;
}