#version 410
#define MAX_SIZE 6

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec3 v_pos;
layout (location = 2) in vec3 v_normals;
layout (location = 3) in float rd_light_diffraction;
layout (location = 4) in vec2 pixel_pos;
in vec4 shadowCoord[MAX_SIZE];

out vec4 fragColor;


uniform vec3 cam_pos;

uniform sampler2D u_texture_0;
uniform sampler2DShadow shadowMap[MAX_SIZE];
uniform int number_mat;

//matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

uniform vec3 light_pos[20]; //max number of lights is 10
uniform vec3 light_color[20];
uniform float light_intensity[20];


//light params
float AMBIANT_LIGHT = 0.06;
float STRENGTH_DIFFUSE = 13.0; //the diffuse has more impact

vec2 size_tex = vec2(4096,4096);

float getSample16X(int ind){
    float shadow = 0;
    for (int i = -8; i<=7; i++){
        shadow+=textureProj(shadowMap[i],shadowCoord[ind]+vec4(i%4,int(i/4),0,0));
    }
    return shadow/16;
}

float getShadow(){
    float shadow = 0;
    if (number_mat == 6){
        shadow+=1;
        for (int i = 0; i<number_mat; i++){
            shadow *= getSample16X(i);
        }
    }
    else{
        shadow += getSample16X(0);
    }
    return shadow/number_mat;
}

void main(){
    //lighting
    vec3 TOTAL_SHADING_COLOR = vec3(0.0);
    float DIFFUSE_LIGHT = 0.0;
    float SPECULAR_LIGHT = 0.0;

    vec3 v_cam = normalize(cam_pos-v_pos); //vector3 for the cam vector

    //we iterate through all the lights in the scene (20 max for performance issues)
    int iteration = 0;
    while (iteration<20 && light_intensity[iteration]!=0) {
        //base color light
        float r_col = light_color[iteration].r/255;
        float g_col = light_color[iteration].g/255;
        float b_col = light_color[iteration].b/255;
        vec3 shade = vec3(r_col,g_col,b_col);
        float d_light = sqrt(pow((light_pos[iteration].x-v_pos.x),2)+pow((light_pos[iteration].y-v_pos.y),2)+pow((light_pos[iteration].z-v_pos.z),2));

        //we calculate the diffuse strength (basic intensity based on dot product)
        vec3 v_vector_light = normalize(light_pos[iteration]-v_pos);
        if (dot(v_vector_light,v_normals)>0.002){ //don't add negative lighting
            DIFFUSE_LIGHT += (1/(rd_light_diffraction+(d_light)*4)); //shading based on the distance and a small number
            DIFFUSE_LIGHT *= light_intensity[iteration]*dot(v_vector_light,v_normals); //multiplied by the light intensity and angle

            //specular touch (based on the angle with the light)
            vec3 v_reflect_light = reflect(-(v_vector_light), v_normals);
            if (dot(v_reflect_light,v_cam)>0){
                SPECULAR_LIGHT = pow(dot(v_reflect_light,v_cam), 70); //multiplied to get a specular highlight
            }
            float shadow = getShadow();

            TOTAL_SHADING_COLOR += (shade*((DIFFUSE_LIGHT*STRENGTH_DIFFUSE)+SPECULAR_LIGHT))*(shadow);
        }

        iteration+=1;
    }
    vec3 shading = TOTAL_SHADING_COLOR + vec3(1,1,1)*AMBIANT_LIGHT;
    

    //converting it to color with 255 as max
    vec3 raw_color = texture(u_texture_0, uv_0).rgb;
    float r = raw_color.r/255;
    float g = raw_color.g/255;
    float b = raw_color.b/255;
    vec3 color = vec3(r*shading.r,g*shading.g,b*shading.b)*255;
    
    //gamma correction
    float gamma = 2.2;
    color=pow(color, vec3(gamma));
    color=pow(color, vec3(1/gamma));


    fragColor = vec4(color, 1.0);
}