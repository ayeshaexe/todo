import { useState } from 'react';
import { TaskFormData } from '../../types';

interface CreateTaskFormProps {
  onCreate: (taskData: TaskFormData) => void;
  onCancel?: () => void;
}

const CreateTaskForm: React.FC<CreateTaskFormProps> = ({ onCreate, onCancel }) => {
  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    description: '',
    completed: false,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title must be less than 200 characters';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be less than 1000 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    onCreate(formData);

    // Reset form after successful creation
    setFormData({
      title: '',
      description: '',
      completed: false,
    });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;

    setFormData(prev => ({ ...prev, [name]: val }));

    // Clear error when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name as keyof typeof errors];
        return newErrors;
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2 className="text-xl font-semibold mb-4">Create New Task</h2>

      <div className="form-field">
        <label htmlFor="title" className="form-label">
          Title *
        </label>
        <input
          id="title"
          name="title"
          type="text"
          value={formData.title}
          onChange={handleChange}
          className={`form-input ${errors.title ? 'border-red-500' : ''}`}
          placeholder="What needs to be done?"
          maxLength={200}
        />
        {errors.title && <p className="error-message">{errors.title}</p>}
      </div>

      <div className="form-field">
        <label htmlFor="description" className="form-label">
          Description (optional)
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          className={`form-input ${errors.description ? 'border-red-500' : ''}`}
          placeholder="Add more details..."
          rows={3}
          maxLength={1000}
        />
        {errors.description && <p className="error-message">{errors.description}</p>}
      </div>

      <div className="flex gap-4 pt-2">
        <button
          type="submit"
          className="btn btn-primary flex-1"
        >
          Create Task
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="btn btn-secondary flex-1"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default CreateTaskForm;