import React, { useState } from 'react';
import { useDrag, useDrop } from 'react-dnd';

const MealPlanner = () => {
  const [meals, setMeals] = useState([
    { id: 1, name: 'Oatmeal', type: 'Breakfast' },
    { id: 2, name: 'Salad', type: 'Lunch' },
    { id: 3, name: 'Grilled Chicken', type: 'Dinner' },
  ]);

  const Meal = ({ meal }: any) => {
    const [, drag] = useDrag(() => ({
      type: 'MEAL',
      item: { id: meal.id },
    }));
    return <div ref={drag} style={{ padding: '8px', border: '1px solid black' }}>{meal.name}</div>;
  };

  const DropZone = ({ type, onDrop }: any) => {
    const [, drop] = useDrop(() => ({
      accept: 'MEAL',
      drop: (item: any) => onDrop(item.id, type),
    }));
    return <div ref={drop} style={{ padding: '8px', border: '1px dashed black', minHeight: '50px' }}>
      {type}
    </div>;
  };

  const handleDrop = (id: number, type: string) => {
    setMeals((prev) =>
      prev.map((meal) => (meal.id === id ? { ...meal, type } : meal))
    );
  };

  return (
    <div>
      <h1>Meal Planner</h1>
      <div style={{ display: 'flex', justifyContent: 'space-around' }}>
        {['Breakfast', 'Lunch', 'Dinner'].map((type) => (
          <DropZone key={type} type={type} onDrop={handleDrop} />
        ))}
      </div>
      <div>
        {meals.map((meal) => (
          <Meal key={meal.id} meal={meal} />
        ))}
      </div>
    </div>
  );
};

export default MealPlanner;
