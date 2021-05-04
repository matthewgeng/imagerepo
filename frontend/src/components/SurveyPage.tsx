import React, { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

import Container from "react-bootstrap/Container";
import Jumbotron from "react-bootstrap/Jumbotron";
import Plotly from "react-plotly.js";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
// survey
import ReactMarkdown from "react-markdown";
import * as Survey from "survey-react";
import "survey-react/modern.css";

import testData from "./testData.json";

interface RouteParams {
  id: string;
}

// for surveyjs
Survey.StylesManager.applyTheme("modern");
// needed to store custom fields in survey js output
Survey.JsonObject.metaData.addClass(
  "customFields",
  [
    {
      name: "trait",
    },
    {
      name: "sentiment",
    },
  ],
  undefined,
  "itemvalue"
);

interface Props {
  json: {};
  css: {};
  onComplete: (res: {
    data: { [key: string]: string | number };
    getQuestionByName: (
      key: string
    ) => { name: string; rows: [{ [key: string]: string | number }] };
  }) => void;
}

interface SurveyRes {
  data: { [key: string]: string | number };
  getQuestionByName: (
    key: string
  ) => { name: string; rows: [{ [key: string]: string | number }] };
}

const choicesProp = Survey.JsonObject.metaData.findProperty("matrix", "rows");
choicesProp.className = "customFields";

const SurveyPage = () => {
  const [desc, setDesc] = useState<string>("# Loading");
  const [surveyQuestions, setSurveyQuestions] = useState<{}>({});
  const [result, setResult] = useState<{}>({});
  const [risk, setRisk] = useState<{}>({});
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [recievedFinalResults, setRecievedFinalResults] = useState<boolean>(
    false
  );
  const [traits, setTraits] = useState<Array<string>>([]);
  const { id } = useParams<RouteParams>();

  const [surveyCss, setSurveyCss] = useState<{}>({});

  // getting survey data
  useEffect(() => {
    axios({
      method: "GET",
      url: `/api/survey/${id}`,
    })
      .then((res) => {
        setDesc(res.data.description);
        setTraits(res.data.traits);
        setSurveyQuestions({ questions: res.data.questions });
        setSurveyCss(res.data.css);
      })
      .catch((e) => {
        console.log(e);
      });
  }, []);

  // parsing survey data + activates submit
  const onComplete = (res: SurveyRes) => {
    console.log(res.data);
    // refactoring data for api call
    setSubmitted(true);
    const newRes: {} = {};
    for (const [k, v] of Object.entries(res.data)) {
      const q = res.getQuestionByName(k);
      if (q.name === "personality") {
        const personality: Array<{}> = [];
        q.rows.forEach((e, i) => {
          personality.push({
            question: e.value,
            trait: e.trait,
            sentiment: e.sentiment,
            // @ts-ignore
            value: res.data[k][e.value],
          });
        });
        // @ts-ignore
        newRes[k] = personality;
      } else if (q.name === "financeKnowledge") {
        // @ts-ignore
        newRes[k] = v[k];
      } else if (q.name === "education") {
        if (v === "low") {
          // @ts-ignore
          newRes.highEducation = false;
          // @ts-ignore
          newRes.mediumEducation = false;
        } else if (v === "medium") {
          // @ts-ignore
          newRes.highEducation = false;
          // @ts-ignore
          newRes.mediumEducation = true;
        } else {
          // @ts-ignore
          newRes.highEducation = true;
          // @ts-ignore
          newRes.mediumEducation = false;
        }
      } else {
        // @ts-ignore
        newRes[k] = v;
      }
    }
    setResult(newRes);
  };

  // submit results
  useEffect(() => {
    if (submitted) {
      axios({
        method: "POST",
        url: `/api/survey/${id}`,
        data: {
          traits: traits,
          questions: result,
        },
      })
        .then((res) => {
          setRisk(res.data);
          setRecievedFinalResults(true);
        })
        .catch((err) => {
          console.log(err);
        });
      setSubmitted(false);
    }
  }, [result]);

  const Spider = () => {
    return (
      <Plotly
        data={[
          {
            type: "scatterpolar",
            // @ts-ignore
            r: Object.values(risk.personality),
            // @ts-ignore
            theta: Object.keys(risk.personality),
            fill: "toself",
          },
        ]}
        layout={{
          polar: {
            radialaxis: {
              visible: true,
              range: [1, 5],
              dtick: 1,
            },
          },
          showlegend: false,
        }}
      />
    );
  };

  const SurveyComponent = ({ json, css, onComplete }: Props) => {
    const surveyRef = useRef();

    // for preloading survey inputs for development
    useEffect(() => {
      if (process.env.REACT_APP_PROD !== "true") {
        if (surveyRef !== null) {
          // @ts-ignore
          surveyRef.current.survey.data = testData;
        }
      }
    }, [surveyRef]);

    return (
      <Survey.Survey
        // @ts-ignore
        ref={surveyRef}
        showCompletedPage={false}
        json={json}
        onComplete={onComplete}
        css={css}
      />
    );
  };

  const Results = () => {
    if (recievedFinalResults) {
      return (
        <Row className="pb-5">
          <Col>
            <ReactMarkdown source={"# Personality Results"} />
            <Spider />
          </Col>
          <Col>
            <ReactMarkdown source={"# Risk Tolerance"} />
            <p>
              risk_tolerance:
              <code>
                {
                  // @ts-ignore
                  risk.risk_tolerance
                }
              </code>
            </p>
            {/* <p>
              savings_ratio:
              <code>
                {
                  // @ts-ignore
                  risk.savings_ratio
                }
              </code>
            </p>
            <p>
              bond_and_mutual_fund_ratio:
              <code>
                {
                  // @ts-ignore
                  risk.bond_and_mutual_fund_ratio
                }
              </code>
            </p>
            <p>
              equity_ratio:
              <code>
                {
                  // @ts-ignore
                  risk.equity_ratio
                }
              </code>
            </p> */}
          </Col>
        </Row>
      );
    } else {
      return null;
    }
  };
  return (
    <Container fluid className="p-5">
      <Jumbotron className="pb-2">
        <ReactMarkdown source={desc} />
      </Jumbotron>
      <Row className="pb-5">
        <Col>
          <SurveyComponent
            json={surveyQuestions}
            css={surveyCss}
            onComplete={onComplete}
          />
        </Col>
      </Row>
      <Results />
      {/* <Row>{<pre>{JSON.stringify(risk, null, 2)}</pre>}</Row> */}
    </Container>
  );
};

export default SurveyPage;
