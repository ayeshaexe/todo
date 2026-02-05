import { Task } from '../../types';
import TaskCard from './TaskCard';

interface TaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onUpdate: (task: Task) => void;
  onDelete: (id: string) => void;
  loading?: boolean;
  emptyMessage?: string;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onEdit,
  onUpdate,
  onDelete,
  loading = false,
  emptyMessage = 'No tasks yet. Create your first task!'
}) => {
  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <div key={index} className="card flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="loading-skeleton w-6 h-6 rounded"></div>
              <div className="flex-1 space-y-2">
                <div className="loading-skeleton h-4 w-3/4"></div>
                <div className="loading-skeleton h-3 w-1/2"></div>
              </div>
            </div>
            <div className="flex gap-2">
              <div className="loading-skeleton w-16 h-8 rounded"></div>
              <div className="loading-skeleton w-16 h-8 rounded"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="card text-center py-8">
        <p className="text-gray-600">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks && Array.isArray(tasks)
        ? tasks
            .filter(task => task.id) // Filter out tasks without an id
            .map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={onEdit}
                onUpdate={onUpdate}
                onDelete={onDelete}
              />
            ))
        : null}
    </div>
  );
};

export default TaskList;