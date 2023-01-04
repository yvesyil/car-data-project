import mongoose from 'mongoose';

const carSchema = new mongoose.Schema({
  make: String,
  model: String,
  year: Number,
  description: String,
  price: {
    currency: String,
    value: Number
  },
  odometer: {
    unit: String,
    value: Number,
  },
  color: String,
  transmission: String,
  fuel_type: String,
  engine_size: Number
});

const carModel = mongoose.model('carModel', carSchema);

export { carModel };