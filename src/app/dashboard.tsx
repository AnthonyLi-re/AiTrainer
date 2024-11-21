import React from 'react';
import { Grid, Card, CardContent, Typography, Button } from '@mui/material';

const Dashboard = () => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h5">AI Trainer</Typography>
            <Typography>Start your workout with live AI feedback!</Typography>
            <Button variant="contained" color="primary" href="/ai-trainer">
              Go to AI Trainer
            </Button>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h5">Meal Planner</Typography>
            <Typography>Plan your meals and track your nutrition.</Typography>
            <Button variant="contained" color="primary" href="/meal-planner">
              Go to Meal Planner
            </Button>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h5">Progress Tracker</Typography>
            <Typography>Track your workouts and meals over time.</Typography>
            <Button variant="contained" color="primary" href="/progress-tracker">
              Go to Progress Tracker
            </Button>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default Dashboard;
