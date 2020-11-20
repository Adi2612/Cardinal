import { useState, useEffect } from "react";
import axios from "axios";
import "./ModelList.css"

const ModelList = () => {
  
  const [containerList, setContainerList] = useState([]);
  
  const getContainerList = async () => {
    let resp = await axios({
      "url": window.location.origin + '/api/list-models/',
      "method": "POST",
      "headers": {
        "content-type": "application/json",
        "cache-control": "no-cache",
      }  
    });
    setContainerList(resp.data);
  }

  useEffect(() => {
    getContainerList();
  }, []);

  return (
    <div className="ModelContainer">
      <div className="Heading"> Deployed Model List </div>
      {containerList.map((item, ket) => (
        <div className="Row">
          <div className="Column">
            {item.model_id}
          </div>
          <div className="Column">
            {item.git_uri}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ModelList;