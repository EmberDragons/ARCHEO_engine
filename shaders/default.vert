#version 410

//in
layout (location = 0) in vec2 in_texcoord;
layout (location = 1) in vec3 in_position;
layout (location = 2) in vec3 in_normales;

//out
out vec2 uv_0;
out vec3 shading;


uniform vec3 cam_pos;

//matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

uniform vec3 light_pos[20]; //max number of lights is 10
uniform float light_intensity[20];
uniform vec3 light_color[20];

float AMBIANT_LIGHT = 0.1;

float random(vec2 st)
{
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main(){
    uv_0 = in_texcoord;
    vec4 v_pos = m_model*vec4(in_position, 1.0); //vector4 for vertex pos
    gl_Position = m_proj*m_view*v_pos;
    
    //lighting
    vec3 TOTAL_SHADING = vec3(0.0);

    vec4 v_normals = m_model*vec4(in_normales, 1.0); //vector4 for the normal of the vertices
    vec4 v_cam = m_model*vec4(cam_pos, 1.0); //vector4 for the cam vector
    int iteration = 0;
    while (iteration<20) {
        float r = light_color[iteration].r/255;
        float g = light_color[iteration].g/255;
        float b = light_color[iteration].b/255;
        vec3 shade = vec3(r,g,b);
        float d_light = sqrt(light_pos[iteration].x*light_pos[iteration].x + light_pos[iteration].y*light_pos[iteration].y + light_pos[iteration].z*light_pos[iteration].z);
        float rd_light_diffraction = random(vec2(in_texcoord*10)); //pseudo-random number generator
        vec4 v_vector_light = normalize(vec4(light_pos[iteration].x-v_pos.x, light_pos[iteration].y-v_pos.y, light_pos[iteration].z-v_pos.z, 1.0));
        if (dot(v_vector_light,v_normals)>0){ //don't add negative lighting
            TOTAL_SHADING += (shade/(rd_light_diffraction+d_light))*(light_intensity[iteration]*(dot(v_vector_light,v_normals)))*(dot(v_vector_light,v_cam)); //shading based on camera view between -1 and 1
        }
        iteration+=1;
    }

    shading = TOTAL_SHADING+AMBIANT_LIGHT;
}
