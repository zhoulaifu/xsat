#include <Python.h>
#include "xsat.h"

static PyObject* R(PyObject* self, PyObject *args){
  
  double b11,b269,b10,b14,b17,b20,b23,b26,b29,b32,b35,b38,b41,b44,b47,b50,b53,b56,b59,b62,b65,b68,b71,b74,b77,b80,b83,b86,b89,b92,b95,b98,b101,b104,b107,b110,b113,b116,b119,b122,b125,b128,b131,b134,b137,b140,b143,b146,b149,b152,b155,b158,b161;
  PyArg_ParseTuple(args,"ddddddddddddddddddddddddddddddddddddddddddddddddddddd", &b11,&b269,&b10,&b14,&b17,&b20,&b23,&b26,&b29,&b32,&b35,&b38,&b41,&b44,&b47,&b50,&b53,&b56,&b59,&b62,&b65,&b68,&b71,&b74,&b77,&b80,&b83,&b86,&b89,&b92,&b95,&b98,&b101,&b104,&b107,&b110,&b113,&b116,&b119,&b122,&b125,&b128,&b131,&b134,&b137,&b140,&b143,&b146,&b149,&b152,&b155,&b158,&b161);
  double _t_8 = DLT(TR32(b11),TR32(b269));
  float _t_10 = TR32(b10)/TR32(b11); 
  float _t_12 = _t_10/TR32(b14); 
  float _t_14 = _t_12/TR32(b17); 
  float _t_16 = _t_14/TR32(b20); 
  float _t_18 = _t_16/TR32(b23); 
  float _t_20 = _t_18/TR32(b26); 
  float _t_22 = _t_20/TR32(b29); 
  float _t_24 = _t_22/TR32(b32); 
  float _t_26 = _t_24/TR32(b35); 
  float _t_28 = _t_26/TR32(b38); 
  float _t_30 = _t_28/TR32(b41); 
  float _t_32 = _t_30/TR32(b44); 
  float _t_34 = _t_32/TR32(b47); 
  float _t_36 = _t_34/TR32(b50); 
  float _t_38 = _t_36/TR32(b53); 
  float _t_40 = _t_38/TR32(b56); 
  float _t_42 = _t_40/TR32(b59); 
  float _t_44 = _t_42/TR32(b62); 
  float _t_46 = _t_44/TR32(b65); 
  float _t_48 = _t_46/TR32(b68); 
  float _t_50 = _t_48/TR32(b71); 
  float _t_52 = _t_50/TR32(b74); 
  float _t_54 = _t_52/TR32(b77); 
  float _t_56 = _t_54/TR32(b80); 
  float _t_58 = _t_56/TR32(b83); 
  float _t_60 = _t_58/TR32(b86); 
  float _t_62 = _t_60/TR32(b89); 
  float _t_64 = _t_62/TR32(b92); 
  float _t_66 = _t_64/TR32(b95); 
  float _t_68 = _t_66/TR32(b98); 
  float _t_70 = _t_68/TR32(b101); 
  float _t_72 = _t_70/TR32(b104); 
  float _t_74 = _t_72/TR32(b107); 
  float _t_76 = _t_74/TR32(b110); 
  float _t_78 = _t_76/TR32(b113); 
  float _t_80 = _t_78/TR32(b116); 
  float _t_82 = _t_80/TR32(b119); 
  float _t_84 = _t_82/TR32(b122); 
  float _t_86 = _t_84/TR32(b125); 
  float _t_88 = _t_86/TR32(b128); 
  float _t_90 = _t_88/TR32(b131); 
  float _t_92 = _t_90/TR32(b134); 
  float _t_94 = _t_92/TR32(b137); 
  float _t_96 = _t_94/TR32(b140); 
  float _t_98 = _t_96/TR32(b143); 
  float _t_100 = _t_98/TR32(b146); 
  float _t_102 = _t_100/TR32(b149); 
  float _t_104 = _t_102/TR32(b152); 
  float _t_106 = _t_104/TR32(b155); 
  float _t_108 = _t_106/TR32(b158); 
  double _t_110 = DLT(_t_108,TR32(b161));
  double _t_112 = DLE(TR32(b161),TR32(b11)); 
  double _t_114 = DLT(TR32(b14),TR32(b269));
  double _t_116 = DLE(TR32(b161),TR32(b14)); 
  double _t_118 = DLT(TR32(b17),TR32(b269));
  double _t_120 = DLE(TR32(b161),TR32(b17)); 
  double _t_122 = DLT(TR32(b20),TR32(b269));
  double _t_124 = DLE(TR32(b161),TR32(b20)); 
  double _t_126 = DLT(TR32(b23),TR32(b269));
  double _t_128 = DLE(TR32(b161),TR32(b23)); 
  double _t_130 = DLT(TR32(b26),TR32(b269));
  double _t_132 = DLE(TR32(b161),TR32(b26)); 
  double _t_134 = DLT(TR32(b29),TR32(b269));
  double _t_136 = DLE(TR32(b161),TR32(b29)); 
  double _t_138 = DLT(TR32(b32),TR32(b269));
  double _t_140 = DLE(TR32(b161),TR32(b32)); 
  double _t_142 = DLT(TR32(b35),TR32(b269));
  double _t_144 = DLE(TR32(b161),TR32(b35)); 
  double _t_146 = DLT(TR32(b38),TR32(b269));
  double _t_148 = DLE(TR32(b161),TR32(b38)); 
  double _t_150 = DLT(TR32(b41),TR32(b269));
  double _t_152 = DLE(TR32(b161),TR32(b41)); 
  double _t_154 = DLT(TR32(b44),TR32(b269));
  double _t_156 = DLE(TR32(b161),TR32(b44)); 
  double _t_158 = DLT(TR32(b47),TR32(b269));
  double _t_160 = DLE(TR32(b161),TR32(b47)); 
  double _t_162 = DLT(TR32(b50),TR32(b269));
  double _t_164 = DLE(TR32(b161),TR32(b50)); 
  double _t_166 = DLT(TR32(b53),TR32(b269));
  double _t_168 = DLE(TR32(b161),TR32(b53)); 
  double _t_170 = DLT(TR32(b56),TR32(b269));
  double _t_172 = DLE(TR32(b161),TR32(b56)); 
  double _t_174 = DLT(TR32(b59),TR32(b269));
  double _t_176 = DLE(TR32(b161),TR32(b59)); 
  double _t_178 = DLT(TR32(b62),TR32(b269));
  double _t_180 = DLE(TR32(b161),TR32(b62)); 
  double _t_182 = DLT(TR32(b65),TR32(b269));
  double _t_184 = DLE(TR32(b161),TR32(b65)); 
  double _t_186 = DLT(TR32(b68),TR32(b269));
  double _t_188 = DLE(TR32(b161),TR32(b68)); 
  double _t_190 = DLT(TR32(b71),TR32(b269));
  double _t_192 = DLE(TR32(b161),TR32(b71)); 
  double _t_194 = DLT(TR32(b74),TR32(b269));
  double _t_196 = DLE(TR32(b161),TR32(b74)); 
  double _t_198 = DLT(TR32(b77),TR32(b269));
  double _t_200 = DLE(TR32(b161),TR32(b77)); 
  double _t_202 = DLT(TR32(b80),TR32(b269));
  double _t_204 = DLE(TR32(b161),TR32(b80)); 
  double _t_206 = DLT(TR32(b83),TR32(b269));
  double _t_208 = DLE(TR32(b161),TR32(b83)); 
  double _t_210 = DLT(TR32(b86),TR32(b269));
  double _t_212 = DLE(TR32(b161),TR32(b86)); 
  double _t_214 = DLT(TR32(b89),TR32(b269));
  double _t_216 = DLE(TR32(b161),TR32(b89)); 
  double _t_218 = DLT(TR32(b92),TR32(b269));
  double _t_220 = DLE(TR32(b161),TR32(b92)); 
  double _t_222 = DLT(TR32(b95),TR32(b269));
  double _t_224 = DLE(TR32(b161),TR32(b95)); 
  double _t_226 = DLT(TR32(b98),TR32(b269));
  double _t_228 = DLE(TR32(b161),TR32(b98)); 
  double _t_230 = DLT(TR32(b101),TR32(b269));
  double _t_232 = DLE(TR32(b161),TR32(b101)); 
  double _t_234 = DLT(TR32(b104),TR32(b269));
  double _t_236 = DLE(TR32(b161),TR32(b104)); 
  double _t_238 = DLT(TR32(b107),TR32(b269));
  double _t_240 = DLE(TR32(b161),TR32(b107)); 
  double _t_242 = DLT(TR32(b110),TR32(b269));
  double _t_244 = DLE(TR32(b161),TR32(b110)); 
  double _t_246 = DLT(TR32(b113),TR32(b269));
  double _t_248 = DLE(TR32(b161),TR32(b113)); 
  double _t_250 = DLT(TR32(b116),TR32(b269));
  double _t_252 = DLE(TR32(b161),TR32(b116)); 
  double _t_254 = DLT(TR32(b119),TR32(b269));
  double _t_256 = DLE(TR32(b161),TR32(b119)); 
  double _t_258 = DLT(TR32(b122),TR32(b269));
  double _t_260 = DLE(TR32(b161),TR32(b122)); 
  double _t_262 = DLT(TR32(b125),TR32(b269));
  double _t_264 = DLE(TR32(b161),TR32(b125)); 
  double _t_266 = DLT(TR32(b128),TR32(b269));
  double _t_268 = DLE(TR32(b161),TR32(b128)); 
  double _t_270 = DLT(TR32(b131),TR32(b269));
  double _t_272 = DLE(TR32(b161),TR32(b131)); 
  double _t_274 = DLT(TR32(b134),TR32(b269));
  double _t_276 = DLE(TR32(b161),TR32(b134)); 
  double _t_278 = DLT(TR32(b137),TR32(b269));
  double _t_280 = DLE(TR32(b161),TR32(b137)); 
  double _t_282 = DLT(TR32(b140),TR32(b269));
  double _t_284 = DLE(TR32(b161),TR32(b140)); 
  double _t_286 = DLT(TR32(b143),TR32(b269));
  double _t_288 = DLE(TR32(b161),TR32(b143)); 
  double _t_290 = DLT(TR32(b146),TR32(b269));
  double _t_292 = DLE(TR32(b161),TR32(b146)); 
  double _t_294 = DLT(TR32(b149),TR32(b269));
  double _t_296 = DLE(TR32(b161),TR32(b149)); 
  double _t_298 = DLT(TR32(b152),TR32(b269));
  double _t_300 = DLE(TR32(b161),TR32(b152)); 
  double _t_302 = DLT(TR32(b155),TR32(b269));
  double _t_304 = DLE(TR32(b161),TR32(b155)); 
  double _t_306 = DLT(TR32(b158),TR32(b269));
  double _t_308 = DLE(TR32(b161),TR32(b158)); 
  double _t_310 = BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( BAND( _t_8,_t_110 ),_t_112 ),_t_114 ),_t_116 ),_t_118 ),_t_120 ),_t_122 ),_t_124 ),_t_126 ),_t_128 ),_t_130 ),_t_132 ),_t_134 ),_t_136 ),_t_138 ),_t_140 ),_t_142 ),_t_144 ),_t_146 ),_t_148 ),_t_150 ),_t_152 ),_t_154 ),_t_156 ),_t_158 ),_t_160 ),_t_162 ),_t_164 ),_t_166 ),_t_168 ),_t_170 ),_t_172 ),_t_174 ),_t_176 ),_t_178 ),_t_180 ),_t_182 ),_t_184 ),_t_186 ),_t_188 ),_t_190 ),_t_192 ),_t_194 ),_t_196 ),_t_198 ),_t_200 ),_t_202 ),_t_204 ),_t_206 ),_t_208 ),_t_210 ),_t_212 ),_t_214 ),_t_216 ),_t_218 ),_t_220 ),_t_222 ),_t_224 ),_t_226 ),_t_228 ),_t_230 ),_t_232 ),_t_234 ),_t_236 ),_t_238 ),_t_240 ),_t_242 ),_t_244 ),_t_246 ),_t_248 ),_t_250 ),_t_252 ),_t_254 ),_t_256 ),_t_258 ),_t_260 ),_t_262 ),_t_264 ),_t_266 ),_t_268 ),_t_270 ),_t_272 ),_t_274 ),_t_276 ),_t_278 ),_t_280 ),_t_282 ),_t_284 ),_t_286 ),_t_288 ),_t_290 ),_t_292 ),_t_294 ),_t_296 ),_t_298 ),_t_300 ),_t_302 ),_t_304 ),_t_306 ),_t_308 ); 
  return Py_BuildValue("d",_t_310);

}

static PyMethodDef methods[] = {
  {"R", R, METH_VARARGS},
  {NULL, NULL}
};

PyMODINIT_FUNC
 initfoo()
{
  PyObject* module= Py_InitModule("foo", methods);
  PyModule_AddIntConstant(module, "dim", 53);
}

