#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec3 v_pos;
layout (location = 2) in vec3 v_normals;
layout (location = 3) in float rd_light_diffraction;

out vec4 fragColor;

uniform vec3 cam_pos;

uniform sampler2D u_texture_0;

uniform vec3 light_pos[20]; //max number of lights is 10
uniform vec3 light_color[20];
uniform float light_intensity[20];
uniform float shininess;

float AMBIANT_LIGHT = 0.1;

void main(){
    //lighting
    vec3 TOTAL_SHADING_COLOR = vec3(0.0);
    float DIFFUSE_LIGHT = 0.0;
    float SPECULAR_LIGHT = 0.0;

    vec3 v_cam = normalize(cam_pos-v_pos); //vector3 for the cam vector

    //we iterate through all the lights in the scene (20 max for performance issues)
    int iteration = 0;
    while (iteration<20) {
        //base color light
        float r = light_color[iteration].r/255;
        float g = light_color[iteration].g/255;
        float b = light_color[iteration].b/255;
        vec3 shade = vec3(r,g,b);
        float d_light = sqrt(pow((light_pos[iteration].x-v_pos.x),2)+pow((light_pos[iteration].y-v_pos.y),2)+pow((light_pos[iteration].z-v_pos.z),2));

        //we calculate the diffuse strength (basic intensity based on dot product)
        vec3 v_vector_light = normalize(light_pos[iteration]-v_pos);
        if (dot(v_vector_light,v_normals)>0){ //don't add negative lighting
            DIFFUSE_LIGHT += (1/(rd_light_diffraction+d_light)); //shading based on the distance and a small number
            DIFFUSE_LIGHT *= light_intensity[iteration]*dot(v_vector_light,v_normals); //multiplied by the light intensity and angle

            //specular touch (based on the angle with the light)
            vec3 v_reflect_light = reflect(-(v_vector_light), v_normals);
            if (dot(v_reflect_light,v_cam)>0){
                SPECULAR_LIGHT += pow(dot(v_reflect_light,v_cam), 100*shininess*light_intensity[iteration]); //multiplied to get a specular highlight
            }
            
        }
        TOTAL_SHADING_COLOR += shade;
        iteration+=1;
    }

    //combining all lights, with specular and diffuse
    vec3 shading = TOTAL_SHADING_COLOR*(AMBIANT_LIGHT+DIFFUSE_LIGHT+SPECULAR_LIGHT);

    //converting it to color with 255 as max
    vec3 raw_color = texture(u_texture_0, uv_0).rgb;
    float r = raw_color.r/255;
    float g = raw_color.g/255;
    float b = raw_color.b/255;
    vec3 color = vec3(r*shading.r,g*shading.g,b*shading.b)*255;
    fragColor = vec4(color, 1.0);
}