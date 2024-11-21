import React, { useEffect, useRef, useState } from 'react';
import * as posedetection from '@tensorflow-models/pose-detection';
import '@tensorflow/tfjs-backend-webgl';
import { Grid, Card, Typography } from '@mui/material';
import './AiTrainer.css';

const AiTrainer = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [detector, setDetector] = useState(null);
  const [reps, setReps] = useState(0);

  useEffect(() => {
    const setupCamera = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    };

    const loadModel = async () => {
      const model = await posedetection.createDetector(
        posedetection.SupportedModels.BlazePose,
        {
          runtime: 'tfjs',
        }
      );
      setDetector(model);
    };

    setupCamera();
    loadModel();
  }, []);

  const detectPose = async () => {
    if (detector && videoRef.current) {
      const poses = await detector.estimatePoses(videoRef.current);
      drawCanvas(poses);
    }
    requestAnimationFrame(detectPose);
  };

  const drawCanvas = (poses) => {
    const ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

    if (poses.length > 0) {
      const keypoints = poses[0].keypoints;
      keypoints.forEach((point) => {
        if (point.score > 0.5) {
          ctx.beginPath();
          ctx.arc(point.x, point.y, 5, 0, 2 * Math.PI);
          ctx.fillStyle = 'red';
          ctx.fill();
        }
      });
    }
  };

  useEffect(() => {
    detectPose();
  }, [detector]);

  return (
    <Grid container spacing={4} style={{ padding: '20px' }}>
      {/* Left Side: Video Feed and Overlay */}
      <Grid item xs={12} md={8}>
        <Card style={{ padding: '20px', position: 'relative' }}>
          <Typography variant="h5" gutterBottom>
            AI Trainer
          </Typography>
          <Typography variant="subtitle1">Reps: {reps}</Typography>
          <div style={{ position: 'relative' }}>
            <video ref={videoRef} className="video-feed" />
            <canvas ref={canvasRef} className="pose-overlay" />
          </div>
        </Card>
      </Grid>

      {/* Right Side: Instructions and Feedback */}
      <Grid item xs={12} md={4}>
        <Card style={{ padding: '20px' }}>
          <Typography variant="h6" gutterBottom>
            Exercise Instructions
          </Typography>
          <Typography variant="body1">
            Make sure to maintain proper posture:
          </Typography>
          <ul>
            <li>Keep your back straight.</li>
            <li>Ensure full range of motion.</li>
            <li>Follow the live feedback.</li>
          </ul>
        </Card>
        <Card style={{ padding: '20px', marginTop: '20px' }}>
          <Typography variant="h6" gutterBottom>
            Live Feedback
          </Typography>
          <Typography variant="body1" color="secondary">
            You're doing great! Keep it up!
          </Typography>
        </Card>
      </Grid>
    </Grid>
  );
};

export default AiTrainer;
