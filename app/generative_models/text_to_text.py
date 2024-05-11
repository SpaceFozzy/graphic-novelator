from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class TextToTextGenerator:
    def __init__(self):
        model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.model = AutoModelForCausalLM.from_pretrained(model_id, load_in_4bit=True, torch_dtype=torch.bfloat16, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.pipe = pipeline(
            task="text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=5000,
        )

    def unload(self):
        del self.model
        del self.tokenizer
        del self.pipe
        torch.cuda.empty_cache()
    
    def generate(self, user_message):
        messages = [
            {"role": "system", "content": "You are a helpful literary assistant specialized in converting text passages into scene descriptions for graphic novels."},
            {"role": "user", "content": user_message}
        ]
        
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        terminators = [
            self.pipe.tokenizer.eos_token_id,
            self.pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        
        outputs = self.pipe(
            prompt,
            max_new_tokens=5000,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        
        return outputs[0]["generated_text"][len(prompt):]
