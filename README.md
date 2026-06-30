## Resources
https://medium.com/@adimodi96/from-logits-to-tokens-9a36feab9cab
## # how LLM work:
how llm work: https://martinfowler.com/articles/function-call-LLM.html
## constraint decoding:
https://www.salmanq.com/blog/llm-constrained-sampling/#
https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output

### best format for constraint decoding
https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output#the-mathematical-formulation
### end

StateInput ClassNext StateStack OperationSTART{KEYPush OBJECTSTART[VALUEPush ARRAYSTARTValue (Str/Num/Bool)OKNoneKEYStringCOLONNoneKEY}OKPop OBJECT (Only if top of stack is OBJECT)COLON:VALUENoneVALUE{KEYPush OBJECTVALUE[VALUEPush ARRAYVALUEValue (Str/Num/Bool)OKNoneVALUE]OKPop ARRAY (Only if top of stack is ARRAY)OK,KEY (if top is OBJECT) / VALUE (if top is ARRAY)NoneOK}OKPop OBJECTOK]OKPop ARRAuY
