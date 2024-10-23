import os
import argparse
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("AZURE_OPENAI_ENDPOINT"))
client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

def create_system_prompt():
  prompt = '''
 ;; Define constants
(defconstant +canvas-width+ 1024)
(defconstant +canvas-height+ 1024)
(defconstant +frame-width+ (/ 1024 6))
(defconstant +frame-height+ (/ 1024 6))
(defconstant +frames-per-row+ 6)

;; Define data structures
(defstruct frame
  image-data    ; Raw image data for the frame
  action-name   ; Name of the action this frame belongs to
  frame-index)  ; Index within the action sequence

(defstruct action
  name          ; Name of the action
  frames)       ; List of frames for this action

;; Main function to generate spritesheet
(defun generate-spritesheet (actions)
  "Generate a spritesheet from a list of actions"
  (let ((canvas (create-blank-canvas +canvas-width+ +canvas-height+))
        (current-row 0))
    
    ;; Process each action
    (dolist (action actions)
      ;; Validate frames count
      (when (> (length (action-frames action)) +frames-per-row+)
        (error "Action ~A has too many frames (max ~D)" 
               (action-name action) +frames-per-row+))
      
      ;; Check if we have enough rows left
      (when (>= (* current-row +frame-height+) +canvas-height+)
        (error "Not enough space for all actions"))
      
      ;; Place frames for current action
      (let ((frames (action-frames action)))
        (loop for frame in frames
              for frame-index from 0
              do
              (let ((x (* frame-index +frame-width+))
                    (y (* current-row +frame-height+)))
                ;; Copy frame to canvas at position (x, y)
                (copy-frame-to-canvas canvas frame x y))))
      
      ;; Move to next row
      (incf current-row)))
  
  ;; Return the completed canvas
  canvas)

;; Helper function to create blank canvas
(defun create-blank-canvas (width height)
  "Create a blank canvas with specified dimensions"
  (make-array (list height width)))

;; Helper function to copy frame to canvas
(defun copy-frame-to-canvas (canvas frame x y)
  "Copy frame data to specified position on canvas"
  (let ((frame-data (frame-image-data frame)))
    (loop for dy from 0 below +frame-height+
          do
          (loop for dx from 0 below +frame-width+
                do
                (setf (aref canvas 
                           (+ y dy) 
                           (+ x dx))
                      (aref frame-data dy dx))))))


(defun 遊戲2d繪圖師
  "你是只會用 Pixel Art 的繪圖師，擅長畫Spritesheet，也擅長畫圖片。"
)


(setq system-role 遊戲2d繪圖師)

(defun 產生Spritesheet圖片 ([user-input String])
  (let* ((actions 
        (list
          (make-action
          :name "attack"
          :frames 6)
          )))
    (輸出圖片 (generate-spritesheet actions user-input))
  )
)

;; Attension: No other comments, just image! 
  '''
  return prompt

def create_user_prompt(text):
  return f'(產生Spritesheet圖片 "{text}")'

def call_llm(prompt):
  """ Call the language model
  Args:
    prompt (str): A prompt for the language model
  Returns:
    The response from the language model
  """
  final_prompt = f'{create_system_prompt()}\n{create_user_prompt(prompt)}\n'
  response =  client.images.generate(
        model="dall-e-3",
        prompt=final_prompt,
        n=1,
        size="1024x1024",
        style="vivid"
    )
  return response

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('text', type=str, help='A text go classify')
  args = parser.parse_args()

  print(args.text)
  answer = call_llm(args.text)
  print(answer)