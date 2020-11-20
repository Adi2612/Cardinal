import { useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import './Inference.css'
const Inference = () => {

  const param = useParams();
  const [modelOutput, setModelOutput] = useState('');
  const [modelInput, setModelInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = async () => {
    if(isLoading === true)
      return
    setIsLoading(true);
    let resp = await axios({
      "url": window.location.origin + "/api/inference/" + param.modelId,
      "method": "POST",
      "headers": {
        "content-type": "application/json",
        "cache-control": "no-cache",
      },
      "data": modelInput
    });
    setIsLoading(false);
    setModelOutput(JSON.stringify(resp.data, null, 1));
  }


  const onTextChange = (e) => {
    setModelInput(e.target.value);
  }

  return (
    <div className="Container">
      <textarea value={modelInput} onChange={onTextChange} placeholder="Type in Json Input here" className="TextArea" />
      <div className="ButtonArea">
        {isLoading &&
          <div> Loading ... </div>
        }
        <button type="submit" onClick={onSubmit}> Submit </button>
      </div>
      <div className="OutputArea">
        <pre>
          {modelOutput}
        </pre>
        {
          modelOutput === '' &&
          "Output will print here"
        }
      </div>
    </div>
  );

}

export default Inference;