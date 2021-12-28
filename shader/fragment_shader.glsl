#version 330

in vec4 fragColor;
in vec2 fragUV;

out vec4 outColor;

uniform int percent;

uniform sampler2D tex1;
uniform sampler2D tex2;

void main()
{
   vec4 texVal1 = texture(tex1, fragUV);
   vec4 texVal2 = texture(tex2, fragUV);

   outColor = fragColor * ( texVal1*(100-percent)/100 + texVal2*percent/100);

}