import { Task } from '../../types';
import CompletionToggle from './CompletionToggle';
import DeleteConfirmation from './DeleteConfirmation';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onUpdate: (task: Task) => void;
  onDelete: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onEdit, onUpdate, onDelete }) => {
  const handleToggleComplete = async (completed: boolean) => {
    const updatedTask = { ...task, completed };
    onUpdate(updatedTask);
  };

  const handleDeleteConfirm = () => {
    onDelete(task.id);
  };

  return (
    <div className="card flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div className="flex items-start gap-3 flex-1 min-w-0">
        <CompletionToggle
          completed={task.completed}
          onToggle={handleToggleComplete}
        />
        <div className="flex-1 min-w-0">
          <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm mt-1 ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
        </div>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => onEdit(task)}
          className="btn btn-secondary text-sm px-3 py-1"
        >
          Edit
        </button>
        <DeleteConfirmation
          onConfirm={handleDeleteConfirm}
          title="Delete Task"
          message={`Are you sure you want to delete "${task.title}"?`}
        >
          <button className="btn btn-secondary text-sm px-3 py-1">Delete</button>
        </DeleteConfirmation>
      </div>
    </div>
  );
};

export default TaskCard;