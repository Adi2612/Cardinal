import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios'
import './Home.css';
import { useParams } from "react-router-dom";


const Home = () => {
  const [gitUrl, setGitUrl] = useState('');
  const [output, setOutput] = useState([]);
  const [modelId, setModelId] = useState('');
  const modelLogRef = useRef(null);
  const params = useParams();
  const handleGitUrl = (event) => {
    setGitUrl(event.target.value);
  }

  const onSubmit = async () => {
    let resp = await axios({
      "url": window.location.origin + "/api/create-model",
      "method": "POST",
      "headers": {
        "content-type": "application/json",
        "cache-control": "no-cache",
      },
      "data": "{\n    \"url\": \"" + gitUrl + "\"\n}"
    });
    setModelId(resp.data);
  }

  useEffect(() => {
    if(modelId !== '') {
      if(modelLogRef.current) {
        clearInterval(modelLogRef.current);
      }
      let modelLogFn = setInterval(async () => {
        try {
          let resp = await axios({
            "url": window.location.origin + '/api/logs/' + modelId,
            "method": "POST",
            "headers": {
              "content-type": "application/json",
              "cache-control": "no-cache",
            }  
          });
          let log_list = resp.data.split('\n');
          setOutput(log_list);
        } catch(e) {
          console.log("Container not created");
        }
        
      }, 3000);
      modelLogRef.current = modelLogFn;
    }
  }, [modelId])


  const checkModelId = async () => {
    try {
      let resp = await axios({
        "url": window.location.origin + '/api/logs/' + params.modelId,
        "method": "POST",
        "headers": {
          "content-type": "application/json",
          "cache-control": "no-cache",
        }  
      });
      setModelId(params.modelId);
    } catch(e) {
      console.log("Model Id is not Valid")
    }
  }

  useEffect(() => {
    if(params.modelId) {
      checkModelId();
    }
  }, [])

  return (
    <div className="App">
      <div className="Input">
        <input id="text" placeholder="git@github.com:Adi2612/reading-comprehender.git" value={gitUrl} onChange={handleGitUrl} /> 
        <button type="submit" id="button" onClick={onSubmit} > Submit </button>
      </div>
      {modelId !== '' &&
      <div className="ModelId">
        {window.location.origin + "/app/inference/" + modelId}
      </div>}
      <div className="Show">
        {output.map((item, i) => (
          <div key={i} className="Item">
            {item}
          </div>
        ))}
        {output.length === 0 &&
        <div style={{textAlign: 'center', color: 'white'}}> Logs will appear here </div>
        }
      </div>
    </div>
  );
}

export default Home;
